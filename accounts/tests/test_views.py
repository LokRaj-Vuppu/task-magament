from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


@pytest.mark.django_db
class TestRegisterAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("register")

    @patch("accounts.views.EmailService.send")
    def test_register_success(self, mock_send):
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Jane Smith",
        }

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["message"] == "User registered successfully"

        assert "access" in response.data["token_details"]
        assert "refresh" in response.data["token_details"]

        assert User.objects.filter(email="test@example.com").exists()

        mock_send.assert_called_once()

    @patch("accounts.views.EmailService.send")
    def test_register_password_mismatch(self, mock_send):
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "wrongpassword",
            "full_name": "Jane Smith",
        }

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert "password" in response.data

        mock_send.assert_not_called()

    @patch("accounts.views.EmailService.send")
    def test_register_duplicate_email(self, mock_send):
        User.objects.create_user(email="test@example.com", password="password123")

        payload = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Jane Smith",
        }

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        mock_send.assert_not_called()


@pytest.mark.django_db
class TestLoginAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("login")

    def test_login_success(self):
        User.objects.create_user(email="test@example.com", password="password123")

        payload = {"email": "test@example.com", "password": "password123"}

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["message"] == "Login Successful"

        assert "access" in response.data["token_details"]

        assert "refresh" in response.data["token_details"]

    def test_login_invalid_password(self):
        User.objects.create_user(email="test@example.com", password="password123")

        payload = {"email": "test@example.com", "password": "wrongpassword"}

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_invalid_email(self):
        payload = {"email": "wrong@test.com", "password": "password123"}

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRefreshTokenAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("token_refresh")

    def test_refresh_token_success(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        refresh = RefreshToken.for_user(user)

        response = self.client.post(self.url, {"refresh": str(refresh)}, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert "access" in response.data

    def test_refresh_invalid_token(self):
        response = self.client.post(
            self.url, {"refresh": "invalidtoken"}, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLogoutAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("logout")

    def test_logout_success(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        refresh = RefreshToken.for_user(user)

        access = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        response = self.client.post(self.url, {"refresh": str(refresh)}, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["message"] == "Logout successful"

    def test_logout_without_authentication(self):
        response = self.client.post(self.url, {"refresh": "sometoken"}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_invalid_refresh_token(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        refresh = RefreshToken.for_user(user)

        access = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        response = self.client.post(self.url, {"refresh": "wrongtoken"}, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
