import pytest
from django.urls import reverse
from rest_framework import status

from applicant_profile.tests.factory import UserContextFactory
from job_profile.tests.factories import JobDescriptionFactory


@pytest.mark.django_db
class TestUserContextPermissions:
    def test_generate_is_authenticated(
        self, authenticated_client, unauthenticated_client
    ):
        client, user = authenticated_client
        unauthenticated_client = unauthenticated_client

        user_context = UserContextFactory(user=user)
        job_description = JobDescriptionFactory(user=user)

        url = reverse("generate_resume_and_cover_letter")

        request_body = {
            "user_context_id": user_context.id,
            "job_description_id": job_description.id,
            "command": "generate_resume",
        }
        response = client.post(url, request_body, format="json")
        assert response.status_code == status.HTTP_200_OK

        bad_request = unauthenticated_client.post(url, request_body, format="json")
        assert (
            bad_request.status_code == status.HTTP_401_UNAUTHORIZED
        ), "Unauthenticated user should not be able to access the endpoint"
