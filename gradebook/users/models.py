from django.db import models
from django.contrib.auth.models import User

class Entries(models.Model):
    """
    Represents an entry in a teacher's gradebook

    id -- django primary key
    student
    assignment
    grade
    teacher -- foreign key to the teacher
    """

    student = models.CharField(max_length = 30)
    assignment = models.CharField(max_length = 60)
    grade = models.FloatField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(models.Model):
    """
    Represents assignments. Pairings of teacher and assignment name are unique

    id -- django primary key
    teacher -- foreign key to the teacher
    name
    """

    class Meta:
        unique_together = (('teacher', 'name'),)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 60)
