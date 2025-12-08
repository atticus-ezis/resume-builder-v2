# accounts/management/commands/update_site.py
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
local_env = BASE_DIR / ".env"
if local_env.exists():
    environ.Env.read_env(local_env)


class Command(BaseCommand):
    help = "Update site domain from environment variable"

    def handle(self, *args, **options):
        site = Site.objects.get(pk=settings.SITE_ID)
        site.domain = env.str("SITE_DOMAIN")
        site.name = env.str("SITE_NAME")
        site.save()
        self.stdout.write(self.style.SUCCESS(f"Site updated to {site.domain}"))
