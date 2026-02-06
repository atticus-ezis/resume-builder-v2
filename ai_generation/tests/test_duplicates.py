import pytest
from django.urls import reverse
from rest_framework import status

from ai_generation.models import Document, DocumentVersion
from ai_generation.tests.factory import DocumentFactory, DocumentVersionFactory
from applicant_profile.tests.factory import UserContextFactory
from job_profile.tests.factories import JobDescriptionFactory


@pytest.mark.django_db
class TestDuplicateDoc:
    def test_duplicate_doc_no_new_version(self, authenticated_client):
        client, user = authenticated_client

        user_context = UserContextFactory(user=user)
        job_description = JobDescriptionFactory(user=user)

        document = DocumentFactory(
            user=user,
            user_context=user_context,
            job_description=job_description,
            document_type="resume",
        )
        existing_document_version = DocumentVersionFactory(
            document=document,
            markdown="test markdown",
            version_name="test version name",
        )

        assert Document.objects.count() == 1
        assert DocumentVersion.objects.count() == 1

        url = reverse("generate_resume_and_cover_letter")
        request_body = {
            "user_context_id": user_context.id,
            "job_description_id": job_description.id,
            "command": "generate_resume",
        }
        response = client.post(url, request_body, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == existing_document_version.id

        #####
