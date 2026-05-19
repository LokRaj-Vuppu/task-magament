import pytest
from django.db import IntegrityError

from accounts.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Jane",
            last_name="Smith",
        )

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"

        # password should be hashed
        assert user.password != "password123"

        assert user.check_password("password123") is True

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com", password="password123"
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    def test_uuid_generated_automatically(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        assert user.uuid is not None

    def test_email_should_be_unique(self):
        User.objects.create_user(email="test@example.com", password="password123")

        with pytest.raises(IntegrityError):
            User.objects.create_user(email="test@example.com", password="password123")

    def test_default_values(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        assert user.is_active is True
        assert user.is_staff is False
        assert user.full_name == ""

    def test_string_representation(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Jane",
            last_name="Smith",
        )

        expected = "Jane Smith | test@example.com"

        assert str(user) == expected

    def test_created_at_and_updated_at(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_without_optional_fields(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        assert user.first_name is None
        assert user.last_name is None
