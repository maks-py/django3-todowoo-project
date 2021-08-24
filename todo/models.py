from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
  """docstring for Todo"models.Model"""
  # Model of todo taks to represent it
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)

  date_created = models.DateTimeField(auto_now_add=True)
  date_complete = models.DateTimeField(null=True, blank=True)

  important = models.BooleanField(default=False)

  def __str__(self):
    return self.title
