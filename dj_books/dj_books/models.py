# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Authors(models.Model):
    id_authors = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    family_name = models.TextField(blank=True, null=True)
    birth = models.IntegerField(blank=True, null=True)
    death = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'


class Books(models.Model):
    id_books = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    valoration = models.IntegerField(blank=True, null=True)
    read_start = models.DateField(blank=True, null=True)
    read_end = models.DateField(blank=True, null=True)
    id_authors = models.ForeignKey(Authors, models.DO_NOTHING, db_column='id_authors')

    class Meta:
        managed = False
        db_table = 'books'
