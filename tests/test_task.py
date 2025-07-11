import pytest # type: ignore
from datetime import datetime
from src.task_manager.task import Task, Priority, Status

@pytest.mark.unit
class TestTaskCreation:
    """Tests de création de tâches"""
    def test_create_task_minimal(self):
        task = Task("Titre test")
        assert task.title == "Titre test"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert isinstance(task.id, str)
        assert isinstance(task.created_at, datetime)
        assert task.status == Status.TODO
        assert task.project_id is None
        assert task.completed_at is None

    def test_create_task_complete(self):
        task = Task("Titre complet", "Desc", Priority.HIGH)
        assert task.title == "Titre complet"
        assert task.description == "Desc"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO

    def test_create_task_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            Task("")

    def test_create_task_invalid_priority_raises_error(self):
        with pytest.raises(ValueError):
            Task("Titre", priority="INVALID")

@pytest.mark.unit
class TestTaskOperations:
    """Tests des opérations sur les tâches"""
    def setup_method(self):
        self.task = Task("Opérations")

    def test_mark_completed_changes_status(self):
        self.task.mark_completed()
        assert self.task.status == Status.DONE
        assert isinstance(self.task.completed_at, datetime)

    def test_update_priority_valid(self):
        self.task.update_priority(Priority.URGENT)
        assert self.task.priority == Priority.URGENT

    def test_update_priority_invalid_raises_error(self):
        with pytest.raises(ValueError):
            self.task.update_priority("LOW")

    def test_assign_to_project(self):
        self.task.assign_to_project("proj-123")
        assert self.task.project_id == "proj-123"

@pytest.mark.unit
class TestTaskSerialization:
    """Tests de sérialisation JSON"""
    def setup_method(self):
        self.task = Task("Sérialisation", "Desc", Priority.LOW)
        self.task.assign_to_project("p1")
        self.task.mark_completed()

    def test_to_dict_contains_all_fields(self):
        d = self.task.to_dict()
        assert set(d.keys()) == {"id", "title", "description", "priority", "created_at", "status", "project_id", "completed_at"}
        assert isinstance(d["priority"], str)
        assert isinstance(d["created_at"], str)
        assert isinstance(d["status"], str)
        assert isinstance(d["completed_at"], str)

    def test_from_dict_recreates_task(self):
        d = self.task.to_dict()
        t2 = Task.from_dict(d)
        assert t2.title == self.task.title
        assert t2.description == self.task.description
        assert t2.priority == self.task.priority
        assert t2.status == self.task.status
        assert t2.project_id == self.task.project_id
        assert t2.completed_at == self.task.completed_at

@pytest.mark.unit
class TestTaskEdgeCases:
    def test_to_dict_with_minimal_task(self):
        task = Task("Minimal")
        d = task.to_dict()
        assert d["completed_at"] is None
        assert d["project_id"] is None

    def test_from_dict_with_minimal_data(self):
        d = {
            "title": "T",
            "priority": "MEDIUM",
            "created_at": datetime.now().isoformat(),
            "status": "TODO"
        }
        t = Task.from_dict(d)
        assert t.title == "T"
        assert t.priority == Priority.MEDIUM
        assert t.status == Status.TODO
