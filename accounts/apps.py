from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        from django.conf import settings
        from django.contrib.sites.models import Site
        from django.db.utils import OperationalError, ProgrammingError

        try:
            Site.objects.update_or_create(
                id=settings.SITE_ID,
                defaults={"domain": settings.SITE_DOMAIN, "name": settings.SITE_NAME},
            )
        except (OperationalError, ProgrammingError):
            pass
