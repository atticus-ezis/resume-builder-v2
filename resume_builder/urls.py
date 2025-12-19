"""
URL configuration for resume_builder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    CustomPasswordResetConfirmView,
    CustomVerifyEmailView,
    CustomRegisterView,
)
from dj_rest_auth.views import (
    PasswordResetView,
    PasswordChangeView,
    LoginView,
    LogoutView,
    UserDetailsView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import ResendEmailVerificationView, RegisterView
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from applicant_profile.views import UserContextViewSet
from job_profile.views import JobDescriptionViewSet
from ai_generation.views import (
    DownloadMarkdownView,
    GenerateResumeAndCoverLetterView,
    UpdateContentView,
    DocumentViewSet,
    DocumentVersionViewSet,
)

router = DefaultRouter()
router.register(r"applicant", UserContextViewSet, basename="applicant")
router.register(r"job", JobDescriptionViewSet, basename="job")
router.register(r"document", DocumentViewSet, basename="document")
router.register(
    r"document-version", DocumentVersionViewSet, basename="document-version"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("applicant/", include("applicant_profile.urls")),
    path(
        "accounts/", include("allauth.account.urls")
    ),  # Required for account_confirm_email URL name
    path("accounts/social/", include("allauth.socialaccount.urls")),
    path(
        "api/",
        include(
            [
                path(
                    "accounts/",
                    include(
                        [
                            # registration / confirm email
                            path(
                                "registration/",
                                CustomRegisterView.as_view(),
                                name="register",
                            ),
                            path(
                                "registration/resend-email/",
                                ResendEmailVerificationView.as_view(),
                                name="resend_email",
                            ),
                            path(
                                "registration/verify-email/",
                                CustomVerifyEmailView.as_view(),
                                name="custom_verify_email",
                            ),
                            # basic
                            path("login/", LoginView.as_view(), name="login"),
                            path("logout/", LogoutView.as_view(), name="logout"),
                            path(
                                "user/", UserDetailsView.as_view(), name="user_details"
                            ),
                            path(
                                "token/refresh/",
                                get_refresh_view().as_view(),
                                name="token_refresh",
                            ),
                            path(
                                "token/verify/",
                                TokenVerifyView.as_view(),
                                name="token_verify",
                            ),
                            # reset password
                            path(
                                "password/reset/",
                                PasswordResetView.as_view(),
                                name="rest_password_reset",
                            ),
                            path(
                                "password/reset/confirm/<uidb64>/<token>/",
                                TemplateView.as_view(
                                    template_name="accounts/password_reset_confirm.html"
                                ),
                                name="password_reset_confirm",  # placeholder
                            ),
                            path(
                                "password/reset/confirm/",
                                CustomPasswordResetConfirmView.as_view(),
                                name="custom_password_reset_confirm",
                            ),
                            path(
                                "password/change/",
                                PasswordChangeView.as_view(),
                                name="password_change",
                            ),
                        ]
                    ),
                ),
                path("context/", include(router.urls)),
                path(
                    "get-resume-and-cover-letter/",
                    GenerateResumeAndCoverLetterView.as_view(),
                    name="get_resume_and_cover_letter",
                ),
                path(
                    "update-content/",
                    UpdateContentView.as_view(),
                    name="update_content",
                ),
                path(
                    "ai-call/",
                    GenerateResumeAndCoverLetterView.as_view(),
                    name="ai_call",
                ),
                path(
                    "ai-call/update-content/",
                    UpdateContentView.as_view(),
                    name="update_content",
                ),
                path(
                    "download-content/",
                    DownloadMarkdownView.as_view(),
                    name="download_content",
                ),
            ]
        ),
    ),
]
