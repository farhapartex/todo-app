from django.db import models
from django.contrib.auth.models import User


class Status(models.TextChoices):
    HAVE_TO_DO = "have_to_do", "Have To Do"
    WORKING = "working_now", "Working Now"
    BLOCKED = "blocked", "Blocked"
    DONE = "done", "Done"


class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.HAVE_TO_DO)

    def __str__(self):
        return self.name
