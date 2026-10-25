from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class Week(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weeks")
    start_date = models.DateField()
    goal = models.CharField(max_length=200, blank=True)

class Task(models.Model):
    week=models.ForeignKey(Week, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    target_minutes=models.PositiveIntegerField()

class PlannedBlock(models.Model):
    "An event the user want to put"
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="planned_blocks")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class ActualLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="actual_logs")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(blank=True)
    focus = models.PositiveSmallIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self):
        return self.title
    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
