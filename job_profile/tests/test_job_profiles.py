import pytest
from job_profile.tests.factories import JobDescriptionFactory
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestJobProfiles:
    def test_create_job_description(self):
        user = UserFactory()
        print(user)
        job_description = JobDescriptionFactory()
        job_description.user = user
        print(job_description)
        assert job_description.user == user
