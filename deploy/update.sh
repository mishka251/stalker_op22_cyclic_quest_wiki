#!/bin/bash

set -e

python manage.py check
python manage.py migrate --skip-checks --no-input
python manage.py collectstatic --skip-checks --no-input --clear
python manage.py import_data --skip-checks --imported_archive=data/data.zip
python manage.py check
