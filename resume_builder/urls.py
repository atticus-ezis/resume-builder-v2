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
from accounts.views import CustomPasswordResetConfirmView, CustomVerifyEmailView
from dj_rest_auth.views import PasswordResetView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/social/", include("allauth.socialaccount.urls")),
    # dj rest auth
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        TemplateView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",  # placeholder
    ),
    path(
        "dj-rest-auth/password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="custom_password_reset_confirm",
    ),
    # reset email
    path(
        "dj-rest-auth/registration/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="resend_email",
    ),
    path(
        "dj-rest-auth/registration/verify-email/",
        CustomVerifyEmailView.as_view(),
        name="custom_verify_email",
    ),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
