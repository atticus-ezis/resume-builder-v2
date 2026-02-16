# ruff: noqa: E402 — DJANGO_SETTINGS_MODULE must be set before importing Django
import os
import sys
from pathlib import Path

# Project root and Django setup (same pattern as manage.py)
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_builder.settings")

import django
import environ
from django.contrib.auth import get_user_model

django.setup()

# Load .env the same way as settings.py so env.str() etc. work
env = environ.Env()
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(env_file)

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password=env.str("ADMIN_PASSWORD"),
    )
    print("Superuser created")
else:
    print("Superuser already exists")
