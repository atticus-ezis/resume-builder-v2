import pytest
from django.urls import reverse


@pytest.fixture
def create_user_context_url():
    return reverse("applicant-list")


@pytest.fixture
def upload_pdf_url():
    return reverse("applicant-upload-pdf")
