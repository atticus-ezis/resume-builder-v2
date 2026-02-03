from factory.django import DjangoModelFactory
import factory
from ai_generation.models import Document
from accounts.tests.factories import UserFactory
from applicant_profile.tests.factory import UserContextFactory
from job_profile.tests.factories import JobDescriptionFactory


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    user = factory.SubFactory(UserFactory)
    user_context = factory.SubFactory(UserContextFactory)
    job_description = factory.SubFactory(JobDescriptionFactory)
    document_type = "resume"
