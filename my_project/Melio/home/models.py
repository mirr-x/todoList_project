from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Task(models.Model):
    task_list = models.ForeignKey(TaskList, related_name="tasklist", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_list.name
