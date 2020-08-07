from django.core.management.base import BaseCommand
from sys import path
path.append("dj_books/reusing/")
from myconfigparser import MyConfigParser
from text_inputs import input_YN,  input_string

class Command(BaseCommand):
    help = 'Command to dump postgres database'

    def handle(self, *args, **options):
        config=MyConfigParser("/etc/dj_books/settings.conf")
        
        print("Hidden settings are going to be generated")
        ans = input_string("Add you smtp mail password")
        config.cset("smtp", "password")
        
        config.save()
#chown -R apache:apache $DIR
#/etc/init.d/apache2 restart
