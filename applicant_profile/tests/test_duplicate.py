import pytest
from rest_framework import status

from applicant_profile.models import UserContext


@pytest.mark.django_db
class TestDuplicateApplicant:
    """Test context_hash and unique constraint (name + context per user) behavior."""

    def test_duplicate_context_renamed(
        self, authenticated_client, create_user_context_url
    ):
        """POST with same context (same hash), different name: existing is renamed and returned with 200."""
        client, user = authenticated_client
        context = {"summary": "Same content", "skills": ["Python"]}
        name = "First"

        # Create first context
        r1 = client.post(
            create_user_context_url,
            {"context": context, "name": name},
            format="json",
        )
        assert r1.status_code == status.HTTP_201_CREATED
        assert UserContext.objects.filter(user=user).count() == 1

        # Same context, different name -> existing renamed, 200, message in response
        r2 = client.post(
            create_user_context_url,
            {"context": context, "name": "Second name"},
            format="json",
        )
        assert r2.status_code == status.HTTP_200_OK
        assert UserContext.objects.filter(user=user).count() == 1
        assert UserContext.objects.first().name == "Second name"
        assert "message" in r2.data
        assert r2.data["message"] == '"First" changed to "Second name"'

    def test_duplicate_name_rejected(
        self, authenticated_client, create_user_context_url
    ):
        client, user = authenticated_client
        context = {"summary": "Same content", "skills": ["Python"]}
        name = "First"

        # Create first context
        r1 = client.post(
            create_user_context_url,
            {"context": context, "name": name},
            format="json",
        )
        assert r1.status_code == status.HTTP_201_CREATED
        assert UserContext.objects.filter(user=user).count() == 1

        r2 = client.post(
            create_user_context_url,
            {"context": "this is new content", "name": name},
            format="json",
        )

        assert r2.status_code == status.HTTP_400_BAD_REQUEST
        assert UserContext.objects.filter(user=user).count() == 1
        assert "name" in r2.data
        assert "already" in str(r2.data["name"]).lower()

    def test_different_user_same_context_allowed(
        self, authenticated_client, create_user_context_url
    ):
        """Same context and name but different user is allowed (no duplicate)."""
        from accounts.tests.factories import UserFactory

        client, user1 = authenticated_client
        context = {"same": "content"}
        name = "Same Name"

        r1 = client.post(
            create_user_context_url,
            {"context": context, "name": name},
            format="json",
        )
        assert r1.status_code == status.HTTP_201_CREATED

        # Second user can create same context/name
        user2 = UserFactory()
        client.force_authenticate(user=user2)
        r2 = client.post(
            create_user_context_url,
            {"context": context, "name": name},
            format="json",
        )
        assert r2.status_code == status.HTTP_201_CREATED
        assert UserContext.objects.filter(user=user1).count() == 1
        assert UserContext.objects.filter(user=user2).count() == 1
