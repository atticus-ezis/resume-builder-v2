import pytest
from rest_framework.test import APIClient
from accounts.tests.factories import UserFactory
from accounts.tests.conftest import (
    generate_uid_and_token,
    generate_email_verification_token,
)


@pytest.mark.django_db
class TestUserRegistration:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_registration_success(self, registration_url):
        response = APIClient().post(
            registration_url,
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        assert response.status_code == 201, (
            f"expected 201 but got {response.status_code}"
        )
        assert response.cookies.get("access_token") is not None, "missing access token"
        assert response.cookies.get("refresh_token") is not None, (
            "missing refresh token"
        )

    def test_confirm_email_verification(self, confirm_email_verification_url):
        user = UserFactory()
        email_verification_token = generate_email_verification_token(user.email)
        response = APIClient().post(
            confirm_email_verification_url,
            {
                "key": email_verification_token,
            },
        )
        assert response.status_code == 200, (
            f"expected 200 but got {response.status_code}"
        )
        assert response.data["logged_in"] is True, "loggin status not updated"

        assert response.cookies.get("access_token") is not None, "missing access token"
        assert response.cookies.get("refresh_token") is not None, (
            "missing refresh token"
        )

    def test_confirm_password_reset(self, confirm_password_reset_url):
        user = UserFactory()
        uid, token = generate_uid_and_token(user)
        response = APIClient().post(
            confirm_password_reset_url,
            {
                "uid": uid,
                "token": token,
                "new_password1": "new_password",
                "new_password2": "new_password",
            },
        )
        assert response.status_code == 200, (
            f"expected 200 but got {response.status_code}"
        )
        assert response.data["detail"] == "Password has been reset.", (
            f"This response isn't expected: {response.data['detail']}"
        )
        assert response.data["logged_in"] is True, "loggin status not updated"

        assert response.cookies.get("access_token") is not None, "missing access token"
        assert response.cookies.get("refresh_token") is not None, (
            "missing refresh token"
        )
