#!/bin/bash
dropdb -U postgres mylibrary_borrar
createdb -U postgres mylibrary_borrar
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver