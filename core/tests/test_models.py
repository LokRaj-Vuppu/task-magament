import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from core.models import Task, TaskAttachment, TaskPriority, TaskStatus


@pytest.mark.django_db
class TestTaskModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@example.com", password="password123", full_name="Jane Smith"
        )

    def test_create_task(self, user):
        task = Task.objects.create(
            user=user,
            title="Learn Django Testing",
            description="Practice pytest",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        )

        assert task.id is not None
        assert task.user == user
        assert task.title == "Learn Django Testing"
        assert task.description == "Practice pytest"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.IN_PROGRESS

    def test_uuid_auto_generated(self, user):
        task = Task.objects.create(user=user, title="Task")

        assert task.uuid is not None

    def test_default_priority_and_status(self, user):
        task = Task.objects.create(user=user, title="Task")

        # Your model currently uses strings rather than enum values
        assert task.priority == "Low"
        assert task.status == "Yet To Start"

    def test_string_representation(self, user):
        task = Task.objects.create(
            user=user,
            title="Learn Testing",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        )

        expected = "Jane Smith | Learn Testing | High | In Progress"

        assert str(task) == expected

    def test_created_updated_fields(self, user):
        task = Task.objects.create(user=user, title="Task")

        assert task.created_at is not None
        assert task.updated_at is not None


@pytest.mark.django_db
class TestTaskAttachmentModel:
    @pytest.fixture
    def task(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123", full_name="Jane Smith"
        )

        return Task.objects.create(user=user, title="Task")

    def test_create_attachment(self, task):
        file = SimpleUploadedFile(
            "test.pdf", b"dummy content", content_type="application/pdf"
        )

        attachment = TaskAttachment.objects.create(task=task, file=file)

        assert attachment.id is not None
        assert attachment.task == task

        # check extension only
        assert attachment.file.name.endswith(".pdf")

    def test_attachment_uuid_generated(self, task):
        file = SimpleUploadedFile("test.pdf", b"dummy content")

        attachment = TaskAttachment.objects.create(task=task, file=file)

        assert attachment.uuid is not None

    def test_attachment_string_representation(self, task):
        file = SimpleUploadedFile("resume.pdf", b"dummy content")

        attachment = TaskAttachment.objects.create(task=task, file=file)

        string_repr = str(attachment)

        assert "Jane Smith" in string_repr
        assert ".pdf" in string_repr

    def test_delete_task_deletes_attachment(self, task):
        file = SimpleUploadedFile("test.pdf", b"dummy content")

        attachment = TaskAttachment.objects.create(task=task, file=file)

        task.delete()

        assert TaskAttachment.objects.filter(id=attachment.id).count() == 0
