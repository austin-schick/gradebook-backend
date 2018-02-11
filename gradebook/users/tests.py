from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from gradebook.users.models import *

class RegisterTest(APITestCase):
    '''
    Uses default tearDown function to roll back database after each test
    function
    '''

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

class LoginTest(APITestCase):
    '''
    Uses default tearDown function to roll back database after each test
    function
    '''

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

    def test_login(self):
        '''
        Testing that a correct username and password causes a successful login
        '''
        data = {
            "username": self.username,
            "password": self.password0
        }
        response = self.client.post(
            "/api/obtain_token", data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(('token' in response.data), True)
        self.assertNotEqual(response.data['token'], '')

        '''
        Testing that an incorrect password causes a failed login
        '''
        data = {
            "username": self.username,
            "password": self.password1
        }
        response = self.client.post(
            "/api/obtain_token", data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(('non_field_errors' in response.data), True)
        self.assertEqual(response.data['non_field_errors'][0],
                         "Unable to log in with provided credentials.")

class AddEntryTest(APITestCase):
    '''
    Uses default tearDown function to roll back database after each test
    function
    '''

    def setUp(self):
        self.username = "gm1neUoveZhIRLNcRZ2d"

        self.password0 = "hr4j0hIwPbLaFBNPetlL"
        self.password1 = "PnXzZbnSdHQJP1aqLceW"

        self.client = APIClient()

        self.data = {
            "username": self.username,
            "password": self.password0,
        }

        def register():
            self.register_response = self.client.post(
                "/api/register", self.data, format='json'
            )
        def login():
            self.token_response = self.client.post(
                "/api/obtain_token", self.data, format='json'
            )
            self.token = self.token_response.data['token']
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
            self.teacher = User.objects.filter(username=self.username)[0]

        register()
        login()

    def test_add_entry(self):
        data = {
            "student": "gaFEneQQFOgOw1XQrNLd",
            "assignment": "1S69P3grEeGF5Rkxp1JbT4bf8n3LhHE5elYhXHHt",
            "grade": 95.6
        }
        response = self.client.post(
            "/api/add_entry", data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
                Entries.objects.filter(teacher=self.teacher).count(), 1)

        '''
        Test that adding an entry with incomplete data fails
        '''
        data = {
            "student": "gaFEneQQFOgOw1XQrNLd",
            "grade": 95.6
        }
        response = self.client.post(
            "/api/add_entry", self.data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_add(self):
        '''
        Reset auth headers
        '''

        self.client.credentials()

        data = {
            "student": "gaFEneQQFOgOw1XQrNLd",
            "assignment": "1S69P3grEeGF5Rkxp1JbT4bf8n3LhHE5elYhXHHt",
            "grade": 95.6
        }
        response = self.client.post(
            "/api/add_entry", data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetGradebookTest(APITestCase):
    '''
    Uses default tearDown function to roll back database after each test
    function
    '''

    def setUp(self):
        self.username = "gm1neUoveZhIRLNcRZ2d"

        self.password0 = "hr4j0hIwPbLaFBNPetlL"
        self.password1 = "PnXzZbnSdHQJP1aqLceW"

        self.client = APIClient()

        self.data = {
            "username": self.username,
            "password": self.password0,
        }

        def register():
            self.register_response = self.client.post(
                "/api/register", self.data, format='json'
            )
        def login():
            self.token_response = self.client.post(
                "/api/obtain_token", self.data, format='json'
            )
            self.token = self.token_response.data['token']
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
            self.teacher = User.objects.filter(username=self.username)[0]
        def create_entry():
            data = {
                "student": "gaFEneQQFOgOw1XQrNLd",
                "assignment": "1S69P3grEeGF5Rkxp1JbT4bf8n3LhHE5elYhXHHt",
                "grade": 95.6
            }
            self.client.post(
                "/api/add_entry", data, format='json'
            )

        register()
        login()
        create_entry()

    def test_get_gradebook(self):
        response = self.client.get("/api/get_gradebook")

        expected_response = {
            'entries': [
                {'student': 'gaFEneQQFOgOw1XQrNLd',
                 'assignment': '1S69P3grEeGF5Rkxp1JbT4bf8n3LhHE5elYhXHHt',
                 'grade': 95.6
                }
            ]
        }

        self.assertEqual(expected_response, response.data)

        '''
        Reset auth headers
        '''

        self.client.credentials()

        '''
        Test unauthorized request
        '''

        response = self.client.get("/api/get_gradebook")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
