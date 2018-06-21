from django.contrib.auth.models import User,Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from books.models import Book,Author,Valoration



def add_permission(group, model, arrCodename):
    ct = ContentType.objects.get_for_model(model)
    for codename in arrCodename:
        permission = Permission.objects.get(content_type=ct, codename=codename)
        group.permissions.add(permission)
    group.save()



def create_data(apps, schema_editor):
    ctBook = ContentType.objects.get_for_model(Book)
    ctAuthor = ContentType.objects.get_for_model(Author)
    ctValoration = ContentType.objects.get_for_model(Valoration)

    pSearchBook = Permission.objects.create(codename='search_book', name='Can search books', content_type=ctBook)
    pSearchAuthor = Permission.objects.create(codename='search_author', name='Can search authors', content_type=ctAuthor)
    pSearchValoration = Permission.objects.create(codename='search_valoration', name='Can search valorations', content_type=ctValoration)

    user=User.objects.create_user('root', password='root')
    user.is_superuser=True
    user.is_staff=True
    user.save()

    groupWorker,create=Group.objects.get_or_create(name="LibraryWorker")
    add_permission(groupWorker,Book,['change_book','add_book','delete_book','search_book'])
    add_permission(groupWorker,Author,['change_author','add_author','delete_author','search_author'])
    add_permission(groupWorker,Valoration,['change_valoration','add_valoration','delete_valoration','search_valoration'])

    groupUser,create=Group.objects.get_or_create(name="LibraryUser")
    add_permission(groupUser,Book,['search_book'])
    add_permission(groupUser,Author,['search_author'])
    add_permission(groupUser,Valoration,['change_valoration','add_valoration','delete_valoration','search_valoration'])

    userWorker=User.objects.create_user('worker', password='worker')
    userWorker.save()
    groupWorker.user_set.add(userWorker)
    
    userUser=User.objects.create_user('user', password='user')
    userUser.save()
    groupUser.user_set.add(userUser)



def fix_perms(*app_labels):
    def wrapped(apps, schema_editor):
        from django.apps.registry import apps
        from django.contrib.contenttypes.management import create_contenttypes
        from django.contrib.auth.management import create_permissions
        for app in app_labels:
            app_conf = apps.get_app_config(app)
            create_contenttypes(app_conf)#, app_conf.get_models())
            create_permissions(app_conf)#, interactive=False)
    return wrapped


# IMPORTANT Permissions are created when the post_migrate signal fires. This signal is only fired if all migrations in the current run are completed. You cannot depend on the permissions existing within your migration. 

class Migration(migrations.Migration):
    dependencies = [
        ('books', '0004_auto_20180605_1932'),
    ]

    operations = [
        migrations.RunPython(fix_perms("books")),
        migrations.RunPython(create_data),
    ]
