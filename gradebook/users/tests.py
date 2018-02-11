from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class RegisterTest(APITestCase):
    def setUp(self):
        self.username = "gm1neUoveZhIRLNcRZ2d"

        self.password0 = "hr4j0hIwPbLaFBNPetlL"
        self.password1 = "PnXzZbnSdHQJP1aqLceW"

        self.client = APIClient()
        self.data = {
            "username": self.username,
            "password": self.password0,
        }
        self.response = self.client.post(
            "/api/register", self.data, format='json'
        )

    def test_register(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.filter(username=self.username).count(), 1)

    def test_duplicate_registration(self):
        '''
        Testing for duplicate registration with the same username and password
        '''

        data = {
            "username": self.username,
            "password": self.password0,
        }
        response = self.client.post(
            "/api/register", data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        '''
        Testing for duplicate registration with different usernames and
        passwords
        '''

        data = {
            "username": self.username,
            "password": self.password1,
        }
        response = self.client.post(
            "/api/register", data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
