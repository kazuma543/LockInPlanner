from django.db import models


class Event(models.Model):
    "An event the user want to put"
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self):
        return self.title