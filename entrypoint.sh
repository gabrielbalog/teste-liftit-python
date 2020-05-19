#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z db 5432; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$DEBUG" = 1 ]; then
  echo "Running pre-script for Django..."

  python manage.py migrate --noinput
  python manage.py initgroups
  python manage.py collectstatic --no-input --clear

  echo "Pre-script finished"
fi


exec "$@"
