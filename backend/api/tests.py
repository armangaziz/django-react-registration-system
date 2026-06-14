from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserTests(APITestCase):

    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "test12345"
        }

        response = self.client.post("/api/user/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login(self):
        User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "test12345"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_current_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        self.client.force_authenticate(user=user)

        response = self.client.get("/api/user/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_admin_user_list(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin12345"
        )

        self.client.force_authenticate(user=admin)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)