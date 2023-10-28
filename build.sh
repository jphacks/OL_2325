#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python peek/manage.py collectstatic --no-input
python peek/manage.py migrate
python peek/manage.py superuser