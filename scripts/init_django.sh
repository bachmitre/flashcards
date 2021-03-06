#!/bin/bash

set -e

if [ "$ENV" = "local" ]; then

    # give it some time ...
    echo "Giving postgres some startup time ..."
    sleep 5

    PGPASSWORD="$DB_PASSWORD"

    #until psql -h "$DB_HOST" -U "$DB_USER" -c '\l'; do
    #  >&2 echo "Postgres is unavailable - sleeping"
    #  sleep 1
    #done

fi;

>&2 echo "Migrating database1 ..."

python manage.py makemigrations --merge --noinput

>&2 echo "Migrating database2 ..."

python manage.py makemigrations --noinput

>&2 echo "Migrating database3 ..."

python manage.py migrate --noinput

>&2 echo "Creating some data ...."

export PYTHONPATH=/app:/usr/local/lib/python3.9/site-packages/
export DJANGO_SETTINGS_MODULE=core.settings

python scripts/init_db.py


if [ "$ENV" = "local" ]; then
    python manage.py runserver 0.0.0.0:8000

else
    python manage.py collectstatic --noinput
    cd /app
    exec gunicorn core.wsgi:application \
        --name webserver \
        --bind 0.0.0.0:8080 \
        --workers 10 \
        --log-level=info
fi;
