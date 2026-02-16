#!/bin/sh
set -e
# Render sets PORT; default 8000 for local/Docker
PORT="${PORT:-8000}"
echo "Running migrations..."
python manage.py migrate
echo "Creating superuser..."
python create_superuser.py
echo "Starting gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn resume_builder.wsgi:application --bind "0.0.0.0:${PORT}" --workers "${GUNICORN_WORKERS:-1}"
