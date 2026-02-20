from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(_setup_site, sender=self)


def _setup_site(sender, **kwargs):
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
