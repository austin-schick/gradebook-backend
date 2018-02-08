from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from gradebook.users.models import Entries
from gradebook.users.serializers import TeacherSerializer
from django.http import JsonResponse
import json

class GetGradebook(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = request.user.entries_set.all().values("student",
                                                         "assignment",
                                                         "grade")
        queryset_list = list(queryset)
        out_dict = {"entries": queryset_list}

        return Response(out_dict, content_type="application/json")

class AddTeacher(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TeacherSerializer

    def post(self, request):
        print(request.data)

        def validate_request_data(rd):
            return ("username" in rd and "password" in rd)

        if not validate_request_data(request.data):
            return Response(status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username = request.data['username'],
                                        password = request.data['password'])

        return Response(status.HTTP_200_OK)

class AddEntry(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        def validate_request_data(rd):
            return ("student" in rd and "assignment" in rd and
                    "grade" in rd)

        if not validate_request_data(request3data):
            return Response(status.HTTP_400_BAD_REQUEST)

        new_entry = Entries(student = request.data['student'],
                            assignment = request.data['assignment'],
                            grade = request.data['grade'],
                            teacher = request.user)
        new_entry.save()
        return Response(status.HTTP_200_OK)
