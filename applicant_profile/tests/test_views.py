import pytest
from rest_framework import status
from applicant_profile.models import UserContext


@pytest.mark.django_db
class TestApplicantProfileViews:
    def test_confirm_context_authenticated(
        self, authenticated_client, create_user_context_url
    ):
        client, user = authenticated_client
        text = "This is a test text"
        name = "Test Context"
        response = client.post(
            create_user_context_url,
            {
                "context": text,
                "name": name,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert UserContext.objects.count() == 1
        assert UserContext.objects.first().context == text
        assert UserContext.objects.first().name == name
        assert UserContext.objects.first().user == user

    def test_confirm_context_unauthenticated(
        self, unauthenticated_client, create_user_context_url
    ):
        client = unauthenticated_client
        text = "This is a test text"
        name = "Test Context"
        response = client.post(
            create_user_context_url,
            {
                "context": text,
                "name": name,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert UserContext.objects.count() == 0
