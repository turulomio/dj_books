# Generated by Django 3.1 on 2020-08-09 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_mine_20200807_0901_permissions_to_groups'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('statistics_global', 'Can see global statistics'), ('statistics_user', 'Can see user statistics'), ('search_book', 'Can search books'), ('search_author', 'Can search authors'), ('search_valoration', 'Can search valorations'), ('database_all_view', 'Can see a view with all database'))},
        ),
    ]