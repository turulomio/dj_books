from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import migrations
from books.models import Book, Author, Valoration
from django.contrib.auth.models import User, Group, Permission


class Command(BaseCommand):
    help = 'Create default users and permissions'

    def add_arguments(self, parser):
        parser.add_argument('--add_example_users',help ="Create example users: user and worker", action='store_true', default=False)

    def handle(self, *args, **options):
        ctBook = ContentType.objects.get_for_model(Book)
        ctAuthor = ContentType.objects.get_for_model(Author)
        ctValoration = ContentType.objects.get_for_model(Valoration)

        Permission.objects.create(codename='search_book', name='Can search books', content_type=ctBook)
        Permission.objects.create(codename='search_author', name='Can search authors', content_type=ctAuthor)
        Permission.objects.create(codename='search_valoration', name='Can search valorations', content_type=ctValoration)

        user=User.objects.create_user('root', password='root')
        user.is_superuser=True
        user.is_staff=True
        user.save()

        groupWorker,create=Group.objects.get_or_create(name="LibraryWorker")
        self.add_permission(groupWorker,Book,['change_book','add_book','delete_book','search_book'])
        self.add_permission(groupWorker,Author,['change_author','add_author','delete_author','search_author'])
        self.add_permission(groupWorker,Valoration,['change_valoration','add_valoration','delete_valoration','search_valoration'])

        groupUser,create=Group.objects.get_or_create(name="LibraryUser")
        self.add_permission(groupUser,Book,['search_book'])
        self.add_permission(groupUser,Author,['search_author'])
        self.add_permission(groupUser,Valoration,['change_valoration','add_valoration','delete_valoration','search_valoration'])


        self.stdout.write(self.style.SUCCESS('Successfully created default permissions'))
        self.stdout.write(self.style.SUCCESS('Successfully created user root with password root. Change it inmediatly'))


        if options['add_example_users']==True:
            userWorker=User.objects.create_user('worker', password='changeme')
            userWorker.save()
            groupWorker.user_set.add(userWorker)

            userUser=User.objects.create_user('user', password='changeme')
            userUser.save()
            groupUser.user_set.add(userUser)
            self.stdout.write(self.style.SUCCESS('Successfully created users: user and worker with password changeme'))

    def add_permission(self, group, model, arrCodename):
        ct = ContentType.objects.get_for_model(model)
        for codename in arrCodename:
            permission = Permission.objects.get(content_type=ct, codename=codename)
            group.permissions.add(permission)
        group.save()
