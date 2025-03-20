from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class Command(BaseCommand):
    help = "Setup periodic tasks"

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.DAYS)

        try:
            task, created = PeriodicTask.objects.get_or_create(
                name="Deactivate inactive users",
                defaults={
                    "interval": schedule,
                    "task": "deactivate_inactive_users",
                    "kwargs": json.dumps({}),
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS("Created periodic task: Deactivate inactive users"))
            else:
                self.stdout.write(self.style.WARNING("Periodic task already exists"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"e"))
