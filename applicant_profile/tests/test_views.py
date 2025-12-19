import pytest
from rest_framework import status
from applicant_profile.models import UserContext


@pytest.mark.django_db
class TestApplicantProfileViews:
    def test_confirm_context_authenticated(
        self, authenticated_client, create_user_context_url
    ):
        client, user = authenticated_client
        context = {
            "experience": "Chilis",
            "position": "Server",
            "location": "San Diego, CA",
        }
        name = "Test Context"
        response = client.post(
            create_user_context_url,
            {
                "context": context,
                "name": name,
            },
            content_type="application/json",
        )
        type
        # Debug: print error if status is not 201
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Error response: {response.status_code}")
            print(f"Error data: {response.data}")
        assert response.status_code == status.HTTP_201_CREATED
        assert UserContext.objects.count() == 1
        assert UserContext.objects.first().context == context
        assert UserContext.objects.first().name == name
        assert UserContext.objects.first().user == user

    def test_confirm_context_unauthenticated(
        self, unauthenticated_client, create_user_context_url
    ):
        client = unauthenticated_client
        context = {
            "experience": "Chilis",
            "position": "Server",
            "location": "San Diego, CA",
        }
        name = "Test Context"
        response = client.post(
            create_user_context_url,
            {
                "context": context,
                "name": name,
            },
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert UserContext.objects.count() == 0
