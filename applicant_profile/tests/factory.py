from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from applicant_profile.models import UserContext
from accounts.tests.factories import UserFactory


class UserContextFactory(DjangoModelFactory):
    class Meta:
        model = UserContext

    context = Faker("json")
    name = Faker("name")
    user = SubFactory(UserFactory)
