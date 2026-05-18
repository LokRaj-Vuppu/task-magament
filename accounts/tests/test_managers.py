import pytest

from accounts.models import User


@pytest.mark.django_db
class TestUserManager:
    def test_create_user_success(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        assert user.email == "test@example.com"
        assert user.check_password("password123")

        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_without_email(self):
        with pytest.raises(ValueError, match="Email is required"):
            User.objects.create_user(email=None, password="password123")

    def test_email_normalized(self):
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM", password="password123"
        )

        assert user.email == "TEST@example.com"

    def test_create_superuser_success(self):
        user = User.objects.create_superuser(
            email="admin@example.com", password="password123"
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    def test_superuser_password_hashed(self):
        user = User.objects.create_superuser(
            email="admin@example.com", password="password123"
        )

        assert user.password != "password123"

        assert user.check_password("password123")

    def test_create_user_with_extra_fields(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Lok",
            last_name="Raj",
        )

        assert user.first_name == "Lok"
        assert user.last_name == "Raj"
