from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        self.register_url = "/api/auth/register/"

    def test_register_user_success(self):
        payload = {
            "full_name": "Rahul Kumar",
            "email": "rahul@example.com",
            "password": "secret123",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["email"], "rahul@example.com")
        self.assertEqual(response.data["user"]["full_name"], "Rahul Kumar")
        self.assertTrue(User.objects.filter(email="rahul@example.com").exists())

    def test_register_duplicate_email_fails(self):
        User.objects.create_user(
            username="existing",
            email="exists@example.com",
            password="secret123",
        )

        payload = {
            "full_name": "Another User",
            "email": "EXISTS@example.com",
            "password": "secret123",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_login_user_success(self):
        user = User.objects.create_user(
            username="sudeepa",
            email="sudeepa@example.com",
            password="secret123",
            first_name="Sudeepa",
            last_name="Satapathy",
        )

        response = self.client.post(
            self.login_url,
            {"email": "SUDEEPA@example.com", "password": "secret123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["id"], user.id)
        self.assertEqual(response.data["user"]["full_name"], "Sudeepa Satapathy")

    def test_login_user_wrong_password_fails(self):
        User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret123",
        )

        response = self.client.post(
            self.login_url,
            {"email": "tester@example.com", "password": "wrong"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid email or password")

    def test_login_requires_email_and_password(self):
        response = self.client.post(self.login_url, {"email": ""}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email and password are required.")
