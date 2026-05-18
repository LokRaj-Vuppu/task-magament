import pytest

from accounts.models import User
from core.models import Task, TaskPriority, TaskStatus
from core.serializers import (
    CreateTaskRequestValidationSerializer,
    DeleteTaskRequestValidationSerializer,
    TaskSerializer,
    UpdateTaskRequestValidationSerializer,
)


@pytest.mark.django_db
class TestTaskSerializer:
    @pytest.fixture
    def task(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            full_name="Lok Raj",
            last_name="Kumar",
        )

        return Task.objects.create(
            user=user,
            title="Learn Testing",
            description="Practice pytest",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        )

    def test_task_serializer_fields(self, task):
        serializer = TaskSerializer(task)

        data = serializer.data

        assert data["title"] == "Learn Testing"

        assert data["description"] == "Practice pytest"

        assert data["priority"] == TaskPriority.HIGH

        assert data["status"] == TaskStatus.IN_PROGRESS

        assert data["user_email"] == "test@example.com"

        assert data["user_uuid"] is not None

        assert data["task_uuid"] is not None

    def test_user_name_field(self, task):
        serializer = TaskSerializer(task)

        assert serializer.data["user_name"] == "Lok Raj Kumar"


@pytest.mark.django_db
class TestCreateTaskRequestValidationSerializer:
    def test_valid_data(self):
        data = {
            "title": "Task title",
            "description": "Task description",
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.IN_PROGRESS,
        }

        serializer = CreateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid()

    def test_title_required(self):
        data = {"description": "Task description"}

        serializer = CreateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid() is False

        assert "title" in serializer.errors

    def test_empty_title(self):
        data = {"title": ""}

        serializer = CreateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid() is False

    def test_default_values(self):
        data = {"title": "Task"}

        serializer = CreateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid()

        assert serializer.validated_data["priority"] == TaskPriority.LOW

        assert serializer.validated_data["status"] == TaskStatus.YET_TO_START


@pytest.mark.django_db
class TestUpdateTaskRequestValidationSerializer:
    def test_valid_update(self):
        import uuid

        data = {"task_uuid": uuid.uuid4(), "description": "Updated task"}

        serializer = UpdateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid()

    def test_no_update_fields(self):
        import uuid

        data = {"task_uuid": uuid.uuid4()}

        serializer = UpdateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid() is False

        assert "At least one field" in str(serializer.errors)

    def test_missing_task_uuid(self):
        data = {"description": "Updated"}

        serializer = UpdateTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid() is False

        assert "task_uuid" in serializer.errors


@pytest.mark.django_db
class TestDeleteTaskRequestValidationSerializer:
    def test_valid_delete(self):
        import uuid

        data = {"task_uuid": uuid.uuid4()}

        serializer = DeleteTaskRequestValidationSerializer(data=data)

        assert serializer.is_valid()

    def test_missing_task_uuid(self):
        serializer = DeleteTaskRequestValidationSerializer(data={})

        assert serializer.is_valid() is False

        assert "task_uuid" in serializer.errors
