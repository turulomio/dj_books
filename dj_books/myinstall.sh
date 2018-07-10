#!/bin/bash
# DIR must be the absolute path where manage.py is wanted to be
DIR="/var/www/localhost/htdocs/dj_books/"
rm -Rf $DIR
mkdir $DIR
cp -R books/ dj_books/ templates/ locale/ manage.py $DIR
sed "11iimport sys\nsys.path.append('/var/www/localhost/htdocs/dj_books/')" dj_books/wsgi.py > $DIR/dj_books/wsgi.py
sed -e "s/DEBUG = True/DEBUG = False/g" dj_books/settings.py > $DIR/dj_books/settings.py

chown -R apache:apache $DIR
/etc/init.d/apache2 restart