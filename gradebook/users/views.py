from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from gradebook.users.models import Entries
from gradebook.users.serializers import TeacherSerializer, EntriesSerializer

class GetGradebook(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = request.user.entries_set.all().values("student",
                                                         "assignment",
                                                         "grade")
        out_dict = {"entries": list(queryset)}
        return Response(out_dict, content_type="application/json")

class AddTeacher(generics.CreateAPIView):
    """
    POST: Route for registering a new teacher
    """

    permission_classes = (AllowAny, )
    serializer_class = TeacherSerializer

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**serializer.validated_data)
        return Response(status.HTTP_200_OK)

class AddEntry(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EntriesSerializer

    def post(self, request):

        serializer = self.get_serializer_class()(data = request.data)

        if not serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        serializer.save(teacher=request.user)
        return Response(status.HTTP_200_OK)
