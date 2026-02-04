from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from accounts.tests.factories import UserFactory
from applicant_profile.models import UserContext


class UserContextFactory(DjangoModelFactory):
    class Meta:
        model = UserContext

    context = Faker("json")
    name = Faker("name")
    user = SubFactory(UserFactory)
