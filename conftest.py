import pytest
from rest_framework.test import APIClient

from accounts.tests.factories import UserFactory


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def unauthenticated_client():
    client = APIClient()
    return client
