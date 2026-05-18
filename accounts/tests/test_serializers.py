import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_register_serializer_valid_data(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Lok Raj",
        }

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is True

    def test_register_password_mismatch(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "differentpassword",
            "full_name": "Lok Raj",
        }

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert "password" in serializer.errors

    def test_register_creates_user(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Lok Raj",
        }

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid()

        user = serializer.save()

        assert User.objects.count() == 1
        assert user.email == "test@example.com"
        assert user.check_password("password123")

    def test_register_returns_tokens(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        serializer = RegisterSerializer(instance=user)

        data = serializer.data

        assert "access" in data
        assert "refresh" in data

    def test_register_short_password(self):
        data = {
            "email": "test@example.com",
            "password": "12",
            "confirm_password": "12",
            "full_name": "Lok Raj",
        }

        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestLoginSerializer:
    def test_login_valid_credentials(self):
        User.objects.create_user(email="test@example.com", password="password123")

        serializer = LoginSerializer(
            data={"email": "test@example.com", "password": "password123"}
        )

        assert serializer.is_valid()

        assert "access" in serializer.validated_data
        assert "refresh" in serializer.validated_data

    def test_login_invalid_password(self):
        User.objects.create_user(email="test@example.com", password="password123")

        serializer = LoginSerializer(
            data={"email": "test@example.com", "password": "wrongpassword"}
        )

        assert serializer.is_valid() is False

    def test_login_invalid_email(self):
        serializer = LoginSerializer(
            data={"email": "wrong@test.com", "password": "password123"}
        )

        assert serializer.is_valid() is False


@pytest.mark.django_db
class TestLogoutSerializer:
    def test_logout_blacklists_token(self):
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        refresh = RefreshToken.for_user(user)

        serializer = LogoutSerializer(data={"refresh": str(refresh)})

        assert serializer.is_valid()

        serializer.save()

    def test_logout_invalid_token(self):
        serializer = LogoutSerializer(data={"refresh": "invalidtoken"})

        assert serializer.is_valid()

        # assert serializer.errors["refresh"][0] == "Token is invalid"
