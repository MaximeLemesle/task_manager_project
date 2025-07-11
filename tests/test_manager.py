import pytest # type: ignore
from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status
from datetime import datetime

@pytest.mark.unit
class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")

    def test_add_task_returns_id(self):
        task_id = self.manager.add_task("Tâche 1")
        assert isinstance(task_id, str)
        assert any(t.id == task_id for t in self.manager.tasks)

    def test_get_task_existing(self):
        task_id = self.manager.add_task("Tâche 2", "desc", Priority.HIGH)
        task = self.manager.get_task(task_id)
        assert task is not None
        assert task.title == "Tâche 2"
        assert task.priority == Priority.HIGH

    def test_get_task_nonexistent_returns_none(self):
        assert self.manager.get_task("bidon") is None

@pytest.mark.unit
class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        self.manager.add_task("A", priority=Priority.LOW)
        self.manager.add_task("B", priority=Priority.HIGH)
        t3_id = self.manager.add_task("C", priority=Priority.HIGH)
        t3 = self.manager.get_task(t3_id)
        t3.status = Status.DONE

    def test_get_tasks_by_status(self):
        todos = self.manager.get_tasks_by_status(Status.TODO)
        assert all(t.status == Status.TODO for t in todos)
        assert len(todos) == 2

    def test_get_tasks_by_priority(self):
        highs = self.manager.get_tasks_by_priority(Priority.HIGH)
        assert all(t.priority == Priority.HIGH for t in highs)
        assert len(highs) == 2

@pytest.mark.unit
class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        self.manager.add_task("Persist 1")
        self.manager.add_task("Persist 2", priority=Priority.URGENT)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        self.manager.save_to_file()
        mock_file.assert_called_with("test_tasks.json", 'w', encoding='utf-8')
        assert mock_json_dump.called

    @patch('os.path.exists', return_value=True)
    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=json.dumps([{
            "id": "1",
            "title": "T1",
            "description": "",
            "priority": "LOW",
            "created_at": datetime.now().isoformat(),
            "status": "TODO",
            "project_id": None,
            "completed_at": None
        }])
    )
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file, mock_exists):
        mock_json_load.return_value = [
            {"id": "1", "title": "T1", "description": "", "priority": "LOW", "created_at": datetime.now().isoformat(), "status": "TODO", "project_id": None, "completed_at": None}
        ]
        self.manager.load_from_file()
        assert len(self.manager.tasks) == 1
        assert self.manager.tasks[0].title == "T1"

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        self.manager.load_from_file()
        assert self.manager.tasks == []

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_empty_list(self, mock_json_load, mock_file, mock_exists):
        mock_json_load.return_value = []
        self.manager.load_from_file()
        assert self.manager.tasks == []

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=IOError("Erreur de lecture"))
    def test_load_from_file_raises_ioerror(self, mock_json_load, mock_file, mock_exists):
        with pytest.raises(IOError):
            self.manager.load_from_file()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump', side_effect=IOError("Erreur d'écriture"))
    def test_save_to_file_raises_ioerror(self, mock_json_dump, mock_file):
        with pytest.raises(IOError):
            self.manager.save_to_file()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=FileNotFoundError)
    def test_load_from_file_filenotfound(self, mock_json_load, mock_file, mock_exists):
        self.manager.load_from_file()
        assert self.manager.tasks == []

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=ValueError("Erreur de parsing"))
    def test_load_from_file_raises_valueerror(self, mock_json_load, mock_file, mock_exists):
        with pytest.raises(IOError):
            self.manager.load_from_file()

    def test_get_statistics_empty(self):
        manager = TaskManager()
        stats = manager.get_statistics()
        assert stats['total_tasks'] == 0
        assert stats['completed_tasks'] == 0
        for v in stats['tasks_by_priority'].values():
            assert v == 0
        for v in stats['tasks_by_status'].values():
            assert v == 0

    def test_get_statistics_various(self):
        manager = TaskManager()
        manager.add_task("A", priority=Priority.LOW)
        manager.add_task("B", priority=Priority.HIGH)
        t3_id = manager.add_task("C", priority=Priority.HIGH)
        t3 = manager.get_task(t3_id)
        t3.status = Status.DONE
        stats = manager.get_statistics()
        assert stats['total_tasks'] == 3
        assert stats['completed_tasks'] == 1
        assert stats['tasks_by_priority']['LOW'] == 1
        assert stats['tasks_by_priority']['HIGH'] == 2
        assert stats['tasks_by_status']['DONE'] == 1

@pytest.mark.integration
def test_manager_integration_flow():
    manager = TaskManager("test_integration.json")
    id1 = manager.add_task("Tâche intégration", priority=Priority.HIGH)
    manager.save_to_file()
    manager.tasks = []
    manager.load_from_file()
    assert any(t.id == id1 for t in manager.tasks)
