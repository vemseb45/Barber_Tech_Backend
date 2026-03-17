#!/bin/sh

echo "Waiting for postgres..."
sleep 10

echo "Running migrations..."
python manage.py migrate

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 --noreload
