import json
from typing import List, Optional
from .task import Task, Priority, Status
import os

class TaskManager:
    """Gestionnaire principal des tâches"""
    def __init__(self, storage_file="tasks.json"):
        self.storage_file = storage_file
        self.tasks: List[Task] = []

    def add_task(self, title, description="", priority=Priority.MEDIUM):
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task.id

    def get_task(self, task_id) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority]

    def delete_task(self, task_id) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def save_to_file(self, filename=None):
        fname = filename or self.storage_file
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"Erreur lors de la sauvegarde des tâches : {e}")

    def load_from_file(self, filename=None):
        fname = filename or self.storage_file
        if not os.path.exists(fname):
            self.tasks = []
            return
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            raise IOError(f"Erreur lors du chargement des tâches : {e}")

    def get_statistics(self):
        stats = {
            'total_tasks': len(self.tasks),
            'completed_tasks': len([t for t in self.tasks if t.status == Status.DONE]),
            'tasks_by_priority': {},
            'tasks_by_status': {}
        }
        for priority in Priority:
            stats['tasks_by_priority'][priority.name] = len([t for t in self.tasks if t.priority == priority])
        for status in Status:
            stats['tasks_by_status'][status.name] = len([t for t in self.tasks if t.status == status])
        return stats
