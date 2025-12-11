import pytest
from rest_framework.test import APIClient
from django.urls import reverse
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


@pytest.fixture
def create_user_context_url():
    return reverse("applicant-create")


@pytest.fixture
def upload_pdf_url():
    return reverse("applicant-upload-pdf")
