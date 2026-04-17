from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Student

User = get_user_model()


class StudentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = "/api/students/"
        self.add_url = "/api/students/add/"
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="secret123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="secret123",
        )

    def test_students_list_requires_user_id(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "user_id is required.")

    def test_create_and_list_students_for_current_user(self):
        payload = {
            "name": "Sneha",
            "email": "sneha@example.com",
            "phone": "+91 6666666666",
            "grade": "10th Grade",
        }

        create_response = self.client.post(
            f"{self.add_url}?user_id={self.user.id}",
            payload,
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["name"], "Sneha")

        Student.objects.create(
            user=self.other_user,
            name="Other Student",
            email="other@student.com",
            phone="1111111111",
            grade="9",
        )

        list_response = self.client.get(f"{self.list_url}?user_id={self.user.id}")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["email"], "sneha@example.com")

    def test_search_filters_by_name_email_or_grade(self):
        Student.objects.create(
            user=self.user,
            name="Sneha",
            email="sneha@example.com",
            phone="6666666666",
            grade="10",
        )
        Student.objects.create(
            user=self.user,
            name="Rahul",
            email="rahul@example.com",
            phone="7777777777",
            grade="11",
        )

        response = self.client.get(f"{self.list_url}?user_id={self.user.id}&search=sne")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Sneha")

    def test_update_student_only_allows_owner(self):
        owned_student = Student.objects.create(
            user=self.user,
            name="Owned",
            email="owned@example.com",
            phone="1111111111",
            grade="9",
        )
        other_student = Student.objects.create(
            user=self.other_user,
            name="Foreign",
            email="foreign@example.com",
            phone="9999999999",
            grade="8",
        )

        own_update = self.client.put(
            f"/api/students/update/{owned_student.id}/?user_id={self.user.id}",
            {
                "name": "Owned Updated",
                "email": "owned@example.com",
                "phone": "2222222222",
                "grade": "10th Grade",
            },
            format="json",
        )

        self.assertEqual(own_update.status_code, status.HTTP_200_OK)
        self.assertEqual(own_update.data["name"], "Owned Updated")

        denied_update = self.client.put(
            f"/api/students/update/{other_student.id}/?user_id={self.user.id}",
            {
                "name": "Should Fail",
                "email": "fail@example.com",
                "phone": "123",
                "grade": "12",
            },
            format="json",
        )

        self.assertEqual(denied_update.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(denied_update.data["error"], "Student not found")

    def test_delete_student_only_allows_owner(self):
        owned_student = Student.objects.create(
            user=self.user,
            name="Owned",
            email="owned@example.com",
            phone="1111111111",
            grade="9",
        )
        other_student = Student.objects.create(
            user=self.other_user,
            name="Foreign",
            email="foreign@example.com",
            phone="9999999999",
            grade="8",
        )

        delete_response = self.client.delete(
            f"/api/students/delete/{owned_student.id}/?user_id={self.user.id}"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Student.objects.filter(id=owned_student.id).exists())

        denied_response = self.client.delete(
            f"/api/students/delete/{other_student.id}/?user_id={self.user.id}"
        )
        self.assertEqual(denied_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(denied_response.data["error"], "Student not found")
