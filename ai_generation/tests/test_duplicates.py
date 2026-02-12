import pytest
from django.urls import reverse
from rest_framework import status

from ai_generation.models import Document, DocumentVersion
from ai_generation.serializers import handle_integrity_error
from ai_generation.tests.factory import DocumentFactory, DocumentVersionFactory
from applicant_profile.tests.factory import UserContextFactory
from job_profile.tests.factories import JobDescriptionFactory


@pytest.mark.django_db
class TestDuplicateDoc:
    def test_duplicate_version_returns_existing_version(self, authenticated_client):
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
        assert (
            response.data[0]["document_version"]["id"] == existing_document_version.id
        )
        assert response.data[0]["document_version"]["markdown"] == "test markdown"

    def test_integrity_error_raises_validation_error(self, authenticated_client):
        """Duplicate (document, version_name) or (document, context_hash) is caught and converted to ValidationError."""
        from django.db import IntegrityError, transaction

        client, user = authenticated_client
        user_context = UserContextFactory(user=user)
        job_description = JobDescriptionFactory(user=user)
        document = DocumentFactory(
            user=user,
            user_context=user_context,
            job_description=job_description,
            document_type="resume",
        )

        # First version: unique (document, version_name) and (document, context_hash)
        DocumentVersionFactory(
            document=document,
            markdown="unique content a",
            version_name="Version One",
        )
        assert DocumentVersion.objects.filter(document=document).count() == 1

        # Duplicate version_name -> IntegrityError -> handler raises ValidationError
        with transaction.atomic():
            with pytest.raises(Exception) as exc_info:
                DocumentVersion.objects.create(
                    document=document,
                    markdown="different content",
                    version_name="Version One",
                )
        assert isinstance(exc_info.value, IntegrityError)
        with pytest.raises(Exception) as validation_error:
            handle_integrity_error(exc_info.value)
        detail = getattr(validation_error.value, "detail", str(validation_error.value))
        assert "name" in str(detail).lower()

        # Duplicate markdown (same context_hash) -> IntegrityError -> handler raises ValidationError
        DocumentVersionFactory(
            document=document,
            markdown="unique content b",
            version_name="Version Two",
        )
        with transaction.atomic():
            with pytest.raises(Exception) as exc_info2:
                DocumentVersion.objects.create(
                    document=document,
                    markdown="unique content b",
                    version_name="Version Three",
                )
        assert isinstance(exc_info2.value, IntegrityError)
        with pytest.raises(Exception) as validation_error2:
            handle_integrity_error(exc_info2.value)
        detail2 = getattr(
            validation_error2.value, "detail", str(validation_error2.value)
        )
        assert "markdown" in str(detail2).lower()
