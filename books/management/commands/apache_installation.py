from django.core.management.base import BaseCommand
#from subprocess import run
#from os import environ


class Command(BaseCommand):
    help = 'Command to dump postgres database'

    def handle(self, *args, **options):
        pass
#        dt=datetime.now()
#        dts="{}{}{}{}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
#        environ["PGPASSWORD"]= settings.DATABASES['default']['PASSWORD']
#        run("pg_dump -U {0} -h {1} --port {2} {3} > {3}-{4}.sql".format(
#                    settings.DATABASES['default']['USER'], 
#                    settings.DATABASES['default']['HOST'], 
#                    settings.DATABASES['default']['PORT'], 
#                    settings.DATABASES['default']['NAME'], 
#                    dts), 
#                shell=True, 
#                env=environ)

##!/bin/bash
## DIR must be the absolute path where manage.py is wanted to be
#DIR="/var/www/localhost/htdocs/dj_books/"
#rm -Rf $DIR
#mkdir $DIR
#cp -R books/ dj_books/ templates/ locale/ manage.py $DIR
#sed "11iimport sys\nsys.path.append('/var/www/localhost/htdocs/dj_books/')" dj_books/wsgi.py > $DIR/dj_books/wsgi.py
#sed -e "s/DEBUG = True/DEBUG = False/g" dj_books/settings.py > $DIR/dj_books/settings.py
#
#chown -R apache:apache $DIR
#/etc/init.d/apache2 restart
