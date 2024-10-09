#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000