from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from resume_builder.settings import FRONTEND_DOMAIN


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = f"{FRONTEND_DOMAIN}/account/login/google-callback"
    client_class = OAuth2Client
