import factory
from django.contrib.auth.models import User
from faker import Faker
from allauth.account.models import EmailAddress

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        password = extracted if extracted else fake.password()
        self.set_password(password)
        self.save()

    @factory.post_generation
    def create_email_address(self, create, extracted, **kwargs):
        if not create:
            return
        EmailAddress.objects.create(user=self, email=self.email, verified=False)


def user_register_request_factory():
    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    return {
        "email": email,
        "password1": password,
        "password2": password,
        "username": username,
    }
