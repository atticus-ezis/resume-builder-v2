import pytest
from job_profile.tests.factories import JobDescriptionFactory
from accounts.tests.factories import UserFactory
from django.shortcuts import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestJobProfiles:
    def test_create_job_description(self):
        user = UserFactory()
        print(user)
        job_description = JobDescriptionFactory()
        job_description.user = user
        print(job_description)
        assert job_description.user == user

    def test_delete_permissions(self):
        user1 = UserFactory()
        user2 = UserFactory()
        job_description = JobDescriptionFactory()
        job_description.user = user1
        job_description.save()
        assert job_description.user == user1
        assert job_description.user != user2
        client = APIClient()
        client.force_authenticate(user=user2)
        url_delete = reverse("job-detail", args=[job_description.id])
        response = client.delete(url_delete)
        assert response.status_code == 404  # filterset removes it
