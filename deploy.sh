#!/bin/bash

cd /home/user/gpu
sudo git pull origin main --no-rebase
source env/bin/activate --no-input
python manage.py collectstatic
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart ginicorn
