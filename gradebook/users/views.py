from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from gradebook.users.models import Entries
from gradebook.users.serializers import TeacherSerializer, EntriesSerializer
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
        serializer = TeacherSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**serializer.validated_data)
        return Response(status.HTTP_200_OK)

class AddEntry(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        serializer = EntriesSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        serializer.save(teacher=request.user)
        return Response(status.HTTP_200_OK)
