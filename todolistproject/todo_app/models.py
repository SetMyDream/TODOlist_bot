from django.db import models

# Create your models here.
from django.db import models

class Task(models.Model):
    title = models.TextField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
