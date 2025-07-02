from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task
from tasks.views import send_email_notification

class Command(BaseCommand):
    help = 'Sends an email notification for tasks that are due today'

    def handle(self, *args, **kwargs):
     tasks_due_today = Task.objects.filter(deadline__date=timezone.localtime().date())
     for task in tasks_due_today:
        send_email_notification(task.assigned_to.email, task.task_name, task.deadline, task.task_id)


