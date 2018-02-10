from django.db import models
from django.contrib.auth.models import User

class Entries(models.Model):
    student = models.CharField(max_length = 30)
    assignment = models.CharField(max_length = 60)
    grade = models.FloatField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(models.Model):
    class Meta:
        unique_together = (('teacher', 'name'),)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 60)
