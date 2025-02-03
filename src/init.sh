#!/bin/bash

pip install -r requirements.txt

python3 manage.py runserver 8000
 
exec "$@"