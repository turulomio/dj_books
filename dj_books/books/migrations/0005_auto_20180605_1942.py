from django.contrib.auth.models import User,Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from books.models import Book



def create_data(apps, schema_editor):
    user=User.objects.create_user('root', password='root')
    user.is_superuser=True
    user.is_staff=True
    user.save()

    group,create=Group.objects.get_or_create(name="LibraryWorker")

    ct = ContentType.objects.get_for_model(Book)
    permission = Permission.objects.get(content_type=ct, codename='change_book')
    group.permissions.add(permission)
    group.save()




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
