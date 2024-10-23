#!/bin/bash

cd /home/user/gpu
sudo git pull origin main
source env/bin/activate
python manage.py collectstatic --no-input
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
sudo systemctl restart gunicorn
