from datetime import datetime
from enum import Enum
import time
import uuid

class Priority(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    URGENT = 'URGENT'

class Status(Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'

class Task:
    """Une tâche avec toutes ses propriétés"""
    def __init__(self, title, description="", priority=Priority.MEDIUM):
        if not title or not isinstance(title, str):
            raise ValueError("Le titre de la tâche ne peut pas être vide.")
        if not isinstance(priority, Priority):
            raise ValueError("La priorité doit être une instance de Priority.")
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.status = Status.TODO
        self.project_id = None
        self.completed_at = None

    def mark_completed(self):
        self.status = Status.DONE
        self.completed_at = datetime.now()

    def update_priority(self, new_priority):
        if not isinstance(new_priority, Priority):
            raise ValueError("La nouvelle priorité doit être une instance de Priority.")
        self.priority = new_priority

    def assign_to_project(self, project_id):
        self.project_id = project_id

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'created_at': self.created_at.isoformat(),
            'status': self.status.name,
            'project_id': self.project_id,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    @classmethod
    def from_dict(cls, data):
        title = data.get('title')
        description = data.get('description', "")
        priority = Priority[data.get('priority', 'MEDIUM')]
        task = cls(title, description, priority)
        task.id = data.get('id', str(uuid.uuid4()))
        task.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        task.status = Status[data.get('status', 'TODO')]
        task.project_id = data.get('project_id', None)
        completed_at = data.get('completed_at')
        if completed_at:
            task.completed_at = datetime.fromisoformat(completed_at)
        return task
