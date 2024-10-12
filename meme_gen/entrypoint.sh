#!/bin/sh

echo "Making database migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

echo "Seeding database..."
python manage.py loaddata fixtures/meme_template.json
python manage.py loaddata fixtures/funny_template_phrases.json

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000