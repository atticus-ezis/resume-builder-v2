import pytest
import re
from django.urls import reverse

# from django.contrib.auth.tokens import default_token_generator
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from allauth.account.models import EmailConfirmationHMAC, EmailAddress


@pytest.fixture(autouse=True)
def django_test_settings(settings):
    """
    Override email backend for all tests to prevent accidental email sending.
    This runs automatically for all test sessions.
    """
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    return settings


# @pytest.fixture
# def client(user, url, data):
#     return APIClient()


@pytest.fixture
def registration_url():
    return reverse("register")


@pytest.fixture
def confirm_password_reset_url():
    return reverse("custom_password_reset_confirm")


@pytest.fixture
def confirm_email_verification_url():
    return reverse("custom_verify_email")


def generate_email_verification_token(user_email):
    email = EmailAddress.objects.get(email=user_email)
    confirmation = EmailConfirmationHMAC(email)
    return confirmation.key


def generate_uid_and_token(user):
    uid = user_pk_to_url_str(user)
    token = default_token_generator.make_token(user)
    return uid, token


@pytest.fixture
def get_confirmation_link(email_body):
    """Extract confirmation link from email body"""
    # More specific pattern for confirmation email URLs
    url_pattern = (
        r"https?://[^\s]+/dj-rest-auth/registration/account-confirm-email/[^\s/]+"
    )
    match = re.search(url_pattern, email_body)
    if match:
        return match.group(0)
    # Fallback to general URL pattern
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(url_pattern, email_body)
    return urls[0] if urls else None


@pytest.fixture
def get_password_reset_token_and_uid(email_body):
    """Extract token and uid from password reset email URL"""
    # Pattern matches: /users/password/reset/{token}/{uid}
    # or similar patterns in the email
    pattern = r"/users/password/reset/([^/\s]+)/([^/\s]+)"
    match = re.search(pattern, email_body)
    if match:
        token = match.group(1)
        uid = match.group(2)
        return token, uid

    # Alternative pattern: /password/reset/{token}/{uid}
    pattern = r"/password/reset/([^/\s]+)/([^/\s]+)"
    match = re.search(pattern, email_body)
    if match:
        token = match.group(1)
        uid = match.group(2)
        return token, uid

    return None, None
