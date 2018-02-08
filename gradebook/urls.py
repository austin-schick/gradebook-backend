"""
gradebook URL Configuration
"""

from django.conf.urls import url
from gradebook.users.views import *
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^api/register', AddTeacher.as_view()),
    url(r'^api/get_gradebook', GetGradebook.as_view()),
    url(r'^api/add_entry', AddEntry.as_view()),
    url(r'^api/obtain_token', obtain_jwt_token),
    url(r'^api/refresh_token', refresh_jwt_token),
]
