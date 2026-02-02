import logging


from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from dj_rest_auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.registration.views import (
    VerifyEmailView as DjRestVerifyEmailView,
)

logger = logging.getLogger(__name__)


class CSRFExemptLoginView(LoginView):
    """
    Login view with CSRF exemption for REST API usage.
    This allows login without CSRF tokens while keeping CSRF protection for other endpoints.
    """

    permission_classes = [AllowAny]  # Explicitly allow unauthenticated access
    authentication_classes = []  # Disable authentication for login endpoint

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomVerifyEmailView(DjRestVerifyEmailView):
    permission_classes = [AllowAny]
    authentication_classes = []
