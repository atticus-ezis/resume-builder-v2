from factory.django import DjangoModelFactory
from job_profile.models import JobDescription
import factory
from accounts.tests.factories import UserFactory


class JobDescriptionFactory(DjangoModelFactory):
    class Meta:
        model = JobDescription

    company_name = factory.Faker("company")
    job_position = factory.Faker("job")
    job_context = factory.Faker("text")
    updated_at = factory.Faker("date_time")
    user = factory.SubFactory(UserFactory)
