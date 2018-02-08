from django.contrib.auth.models import User
from gradebook.users.models import Entries
from rest_framework import serializers

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', )

class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ('student', 'assignment', 'grade', 'teacher')
