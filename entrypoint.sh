#!/bin/sh
set -e

PORT="${PORT:-8000}"
echo "Running migrations..."
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Creating superuser..."
python create_superuser.py
echo "Starting celery worker in background..."
celery -A resume_builder worker -l info &
echo "Starting gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn resume_builder.wsgi:application --bind "0.0.0.0:${PORT}" --workers "${GUNICORN_WORKERS:-1}" --timeout 120 --preload
