import factory
from factory.django import DjangoModelFactory

from accounts.tests.factories import UserFactory
from ai_generation.models import Document, DocumentVersion
from applicant_profile.tests.factory import UserContextFactory
from job_profile.tests.factories import JobDescriptionFactory


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    user = factory.SubFactory(UserFactory)
    user_context = factory.SubFactory(UserContextFactory)
    job_description = factory.SubFactory(JobDescriptionFactory)
    document_type = "resume"


class DocumentVersionFactory(DjangoModelFactory):
    class Meta:
        model = DocumentVersion

    document = factory.SubFactory(DocumentFactory)
    markdown = factory.Faker("paragraph")
    version_name = factory.Faker("word")
