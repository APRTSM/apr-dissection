#!/bin/bash

pip install -r requirements.txt

python3 manage.py runserver 8006
 
exec "$@"