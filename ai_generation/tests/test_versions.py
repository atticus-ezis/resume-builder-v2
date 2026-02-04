"""Create multiple versions of a document and assert version numbers increment."""

import pytest

from ai_generation.models import DocumentVersion
from ai_generation.tests.factory import DocumentFactory


@pytest.mark.django_db
class TestDocumentVersions:
    def test_version_names_auto_generate(self):
        """Test that version_name auto-generates when not provided."""
        document = DocumentFactory()
        v1 = DocumentVersion.objects.create(document=document, markdown="# v1")
        v2 = DocumentVersion.objects.create(document=document, markdown="# v2")
        v3 = DocumentVersion.objects.create(document=document, markdown="# v3")

        # Format: "CompanyName - document_type - count"
        expected_prefix = str(document)
        assert v1.version_name == f"{expected_prefix} - 1"
        assert v2.version_name == f"{expected_prefix} - 2"
        assert v3.version_name == f"{expected_prefix} - 3"

    def test_custom_version_name(self):
        """Test that custom version_name is used when provided."""
        document = DocumentFactory()
        v1 = DocumentVersion.objects.create(
            document=document, markdown="# v1", version_name="Custom Version"
        )
        assert v1.version_name == "Custom Version"

    def test_custom_name_does_not_affect_auto_generation(self):
        """Test that custom names don't break auto-generation for subsequent versions."""
        document = DocumentFactory()
        v1 = DocumentVersion.objects.create(
            document=document, markdown="# v1", version_name="My Custom Name"
        )
        v2 = DocumentVersion.objects.create(document=document, markdown="# v2")

        assert v1.version_name == "My Custom Name"
        # v2 should auto-generate based on total count (2 versions exist)
        assert v2.version_name == f"{str(document)} - 2"

    def test_version_name_can_be_updated(self):
        """Test that version_name can be updated after creation."""
        document = DocumentFactory()
        v1 = DocumentVersion.objects.create(document=document, markdown="# v1")
        original_name = v1.version_name

        v1.version_name = "Updated Name"
        v1.save()
        v1.refresh_from_db()

        assert v1.version_name == "Updated Name"
        assert v1.version_name != original_name

    # def test_duplicate_doc_no_new_version(self, authenticated_client):
    #     client, user = authenticated_client

    #     user_context = UserContextFactory(user=user)
    #     job_description = JobDescriptionFactory(user=user)

    #     document = DocumentFactory(
    #         user=user,
    #         user_context=user_context,
    #         job_description=job_description,
    #         document_type="resume",
    #     )

    #     assert Document.objects.count() == 1
    #     assert DocumentVersion.objects.count() == 0

    #     url = reverse("generate_resume_and_cover_letter")

    #     request_body = {
    #         "user_context_id": user_context.id,
    #         "job_description_id": job_description.id,
    #         "command": "generate_resume",
    #     }
    #     client.post(url, request_body, format="json")

    #     assert Document.objects.count() == 1
    #     assert DocumentVersion.objects.count() == 1

    # def test_duplicate_doc_with_new_version(self, authenticated_client):
    #     client, user = authenticated_client

    #     user_context = UserContextFactory(user=user)
    #     job_description = JobDescriptionFactory(user=user)

    #     document = DocumentFactory(
    #         user=user,
    #         user_context=user_context,
    #         job_description=job_description,
    #         document_type="resume",
    #     )
    #     document_version = DocumentVersion.objects.create(
    #         document=document,
    #         markdown="# v1",
    #     )

    #     assert Document.objects.count() == 1
    #     assert DocumentVersion.objects.count() == 1

    #     url = reverse("generate_resume_and_cover_letter")

    #     request_body = {
    #         "user_context_id": user_context.id,
    #         "job_description_id": job_description.id,
    #         "command": "generate_resume",
    #     }
    #     response = client.post(url, request_body, format="json")

    #     assert Document.objects.count() == 1
    #     assert DocumentVersion.objects.count() == 1
    #     assert response.data["markdown"] == "# v1"
