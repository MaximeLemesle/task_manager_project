import smtplib
from datetime import datetime
import csv

class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        self.smtp_server = smtp_server
        self.port = port

    def send_task_reminder(self, email, task_title, due_date):
        if not isinstance(email, str) or '@' not in email:
            raise ValueError("Email invalide")
        # Simulation d'envoi (pas de vrai SMTP ici)
        print(f"[SIMULATION] Rappel envoyé à {email} pour la tâche '{task_title}' avant le {due_date}")
        return True

    def send_completion_notification(self, email, task_title):
        if not isinstance(email, str) or '@' not in email:
            raise ValueError("Email invalide")
        print(f"[SIMULATION] Notification de complétion envoyée à {email} pour la tâche '{task_title}'")
        return True

class ReportService:
    """Service de génération de rapports"""
    def generate_daily_report(self, tasks, date=None):
        if date is None:
            date = datetime.now().date()
        else:
            date = date.date() if isinstance(date, datetime) else date
        tasks_today = [t for t in tasks if t.created_at.date() == date]
        report = {
            'date': str(date),
            'total_tasks': len(tasks_today),
            'completed_tasks': len([t for t in tasks_today if t.status.name == 'DONE']),
            'tasks_by_priority': {},
            'tasks_by_status': {}
        }
        from src.task_manager.task import Priority, Status
        for priority in Priority:
            report['tasks_by_priority'][priority.name] = len([t for t in tasks_today if t.priority == priority])
        for status in Status:
            report['tasks_by_status'][status.name] = len([t for t in tasks_today if t.status == status])
        return report

    def export_tasks_csv(self, tasks, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'title', 'description', 'priority', 'created_at', 'status', 'project_id', 'completed_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for task in tasks:
                    writer.writerow(task.to_dict())
        except Exception as e:
            raise IOError(f"Erreur lors de l'export CSV : {e}")
