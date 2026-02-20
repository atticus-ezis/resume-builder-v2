#!/bin/sh
set -e

# Only run web setup when first argument is "web" (migrate, collectstatic, gunicorn)
if [ "$1" = "web" ]; then
    PORT="${PORT:-8000}"
    echo "Running migrations..."
    python manage.py migrate
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    echo "Creating superuser..."
    python create_superuser.py
    echo "Starting gunicorn on 0.0.0.0:${PORT}..."
    exec gunicorn resume_builder.wsgi:application --bind "0.0.0.0:${PORT}" --workers "${GUNICORN_WORKERS:-1}"
fi

# Run Celery worker when first argument is "celery" (no migrate/collectstatic)
if [ "$1" = "celery" ]; then
    exec celery -A resume_builder worker -l info
fi

# Otherwise run whatever command was passed
exec "$@"
