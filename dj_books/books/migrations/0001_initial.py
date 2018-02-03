# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-03 09:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id_authors', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('family_name', models.TextField(blank=True, null=True)),
                ('birth', models.IntegerField(blank=True, null=True)),
                ('death', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'authors',
                'ordering': ['name', 'family_name', 'birth'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id_books', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('valoration', models.IntegerField(blank=True, null=True)),
                ('read_start', models.DateField(blank=True, null=True)),
                ('read_end', models.DateField(blank=True, null=True)),
                ('id_authors', models.ForeignKey(db_column='id_authors', on_delete=django.db.models.deletion.DO_NOTHING, to='books.Author')),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]
