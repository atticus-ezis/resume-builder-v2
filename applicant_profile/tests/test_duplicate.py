import pytest
from rest_framework import status

from applicant_profile.models import UserContext


@pytest.mark.django_db
class TestDuplicateApplicant:
    """Test context_hash and unique constraint (name + context per user) behavior."""

    def test_duplicate_context_rejected(
        self, authenticated_client, create_user_context_url
    ):
        """POST with same context (same hash) as existing returns 400."""
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

        # Same context, different name -> same context_hash -> rejected
        r2 = client.post(
            create_user_context_url,
            {"context": context, "name": "Second name"},
            format="json",
        )
        assert r2.status_code == status.HTTP_400_BAD_REQUEST
        assert UserContext.objects.filter(user=user).count() == 1
        assert "content already exists" in str(r2.data).lower()

        r3 = client.post(
            create_user_context_url,
            {"context": "new context", "name": name},
            format="json",
        )
        assert r3.status_code == status.HTTP_400_BAD_REQUEST
        assert UserContext.objects.filter(user=user).count() == 1
        assert "you already have a context with this name" in str(r3.data).lower()

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
