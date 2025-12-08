from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if "email_confirmation" in template_prefix:
            if "key" in context:
                key = context["key"]
                context["activate_url"] = (
                    f"{settings.FRONTEND_DOMAIN}/users/email/verify/{key}"
                )

        if "password_reset_key" in template_prefix:
            old_url = context.get("password_reset_url")
            token = old_url.split("/")[-2]
            uid = old_url.split("/")[-3]

            context["password_reset_url"] = (
                f"{settings.FRONTEND_DOMAIN}/users/password/reset/{token}/{uid}"
            )

        return super().send_mail(template_prefix, email, context)
