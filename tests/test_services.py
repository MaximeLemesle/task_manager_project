import pytest # type: ignore
from unittest.mock import patch, Mock, mock_open
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority, Status
from datetime import datetime, timedelta

class TestEmailService:
    """Tests du service email avec mocks"""
    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        # Ici, on simule juste l'appel, le print suffit
        result = self.email_service.send_task_reminder("test@mail.com", "Tâche", "2025-01-01")
        assert result is True

    def test_send_task_reminder_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_task_reminder("invalid", "Tâche", "2025-01-01")

    def test_send_completion_notification_success(self):
        result = self.email_service.send_completion_notification("test@mail.com", "Tâche")
        assert result is True

    def test_send_completion_notification_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_completion_notification("invalid", "Tâche")

class TestReportService:
    """Tests du service de rapports"""
    def setup_method(self):
        self.report_service = ReportService()
        now = datetime.now()
        self.tasks = [
            Task("A", priority=Priority.LOW),
            Task("B", priority=Priority.HIGH),
            Task("C", priority=Priority.HIGH)
        ]
        self.tasks[0].created_at = now
        self.tasks[1].created_at = now
        self.tasks[2].created_at = now - timedelta(days=1)
        self.tasks[1].status = Status.DONE

    @patch('src.task_manager.services.datetime')
    def test_generate_daily_report_fixed_date(self, mock_datetime):
        fixed_date = datetime.now().date()
        mock_datetime.now.return_value = datetime.combine(fixed_date, datetime.min.time())
        report = self.report_service.generate_daily_report(self.tasks)
        assert report['date'] == str(fixed_date)
        assert report['total_tasks'] == 2
        assert report['completed_tasks'] == 1
        assert report['tasks_by_priority']['LOW'] == 1
        assert report['tasks_by_priority']['HIGH'] == 1

    @patch('builtins.open', new_callable=mock_open)
    def test_export_tasks_csv(self, mock_file):
        self.report_service.export_tasks_csv(self.tasks, "export.csv")
        mock_file.assert_called_with("export.csv", 'w', newline='', encoding='utf-8')

    @patch('builtins.open', side_effect=IOError("Erreur d'écriture"))
    def test_export_tasks_csv_raises_ioerror(self, mock_file):
        with pytest.raises(IOError):
            self.report_service.export_tasks_csv(self.tasks, "export.csv")

    def test_generate_daily_report_invalid_data(self):
        # Passe une tâche sans attribut created_at
        class Dummy:
            pass
        with pytest.raises(AttributeError):
            self.report_service.generate_daily_report([Dummy()])
