#!/bin/bash
dropdb -U postgres libros_borrar
createdb -U postgres libros_borrar
python3 manage.py migrate
python3 manage.py loaddata fixtures/users.json
python3 manage.py runserver



#  python manage.py dumpdata auth.user -o fixtures/users.json

# DEFAULT ADMIN USER; admin      and changeme
# GUEST USRE: guest changeme