#!/bin/bash

cd /home/user/gpu
git pull origin main
source env/bin/activate
python manage.py collectstatic
#pip install -r requirements.txt
#python manage.py migrate
sudo systemctl restart ginicorn
