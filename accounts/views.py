import logging

from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.registration.views import (
    VerifyEmailView as DjRestVerifyEmailView,
    RegisterView,
)
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password",
        "old_password",
        "new_password1",
        "new_password2",
    ),
)

# Create your views here.


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        access = data.pop("access")
        refresh = data.pop("refresh")

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
            set_jwt_cookies(response, access, refresh)
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class CustomVerifyEmailView(DjRestVerifyEmailView):
    def get_object(self):
        obj = super().get_object()
        self.user = obj.email_address.user
        return obj

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            refresh = RefreshToken.for_user(self.user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            set_jwt_cookies(response, access_token, refresh_token)
            response.data["logged_in"] = True

        except Exception:
            logger.exception(
                "Failed to create/set JWT tokens after email verification for user %s",
            )
            response.data["logged_in"] = False

        return response


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.user

        response = Response(
            {"detail": _("Password has been reset.")},
            status=status.HTTP_200_OK,
        )

        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            set_jwt_cookies(response, access_token, refresh_token)
            response.data["logged_in"] = True
        except Exception:
            logger.exception(
                "Failed to create/set JWT tokens after password reset confirm for user %s",
                user.id if user else "unknown",
            )
            response.data["logged_in"] = False

        return response
