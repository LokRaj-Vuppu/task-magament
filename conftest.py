import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


@pytest.fixture
def user():
    return User.objects.create_user(email="test@example.com", password="password123")


@pytest.fixture
def authenticated_client(user):
    from rest_framework.test import APIClient

    client = APIClient()

    refresh = RefreshToken.for_user(user)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
