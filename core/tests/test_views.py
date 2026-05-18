from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from core.models import Task


@pytest.mark.django_db
class TestTaskViews:
    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@example.com", password="password123", full_name="Lok Raj"
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    @patch("core.views.EmailService.send")
    def test_create_task_success(self, mock_email):
        payload = {
            "title": "Learn Django",
            "description": "Testing APIs",
            "priority": "High",
            "status": "In Progress",
        }

        response = self.client.post(reverse("create_task"), payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["message"] == "Task is created"

        assert Task.objects.filter(title="Learn Django").exists()

        mock_email.assert_called_once()

    @patch("core.views.EmailService.send")
    def test_create_duplicate_task(self, mock_email):
        Task.objects.create(title="Learn Django", user=self.user)

        payload = {"title": "Learn Django"}

        response = self.client.post(reverse("create_task"), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data["message"] == "Task already exists with given title"

        mock_email.assert_not_called()

    def test_create_task_invalid_request(self):
        payload = {"title": ""}

        response = self.client.post(reverse("create_task"), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_all_tasks(self):
        Task.objects.create(title="Task1", user=self.user)

        Task.objects.create(title="Task2", user=self.user)

        response = self.client.get(reverse("get_tasks"))

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["tasks"]) == 2

    @patch("core.views.EmailService.send")
    def test_update_task_success(self, mock_email):
        task = Task.objects.create(title="Task1", user=self.user)

        payload = {
            "task_uuid": str(task.uuid),
            "description": "updated desc",
            "status": "Completed",
        }

        response = self.client.patch(reverse("update_task"), payload, format="json")

        task.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK

        assert task.description == "updated desc"

        assert task.status == "Completed"

        mock_email.assert_called_once()

    def test_update_task_not_found(self):
        import uuid

        payload = {"task_uuid": str(uuid.uuid4()), "description": "updated"}

        response = self.client.patch(reverse("update_task"), payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch("core.views.EmailService.send")
    def test_delete_task_success(self, mock_email):
        task = Task.objects.create(title="Task1", user=self.user)

        response = self.client.delete(
            reverse("delete_task"), {"task_uuid": str(task.uuid)}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        assert not Task.objects.filter(id=task.id).exists()

        mock_email.assert_called_once()

    def test_delete_task_not_found(self):
        import uuid

        response = self.client.delete(
            reverse("delete_task"), {"task_uuid": str(uuid.uuid4())}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_without_authentication(self):
        client = APIClient()

        response = client.get(reverse("get_tasks"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
