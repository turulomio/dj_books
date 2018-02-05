# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from  django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):    
    SPANISH= 'ES'
    ENGLISH = 'EN'
    FRENCH="FR"
    LANGUAGES= (
        (SPANISH, 'Español'),
        (ENGLISH, 'English'),
        (FRENCH, 'Francés')
    )
    language= models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default=ENGLISH,
    )
    user = models.ForeignKey(User)
    
class Author(models.Model):
    id_authors = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    family_name = models.TextField(blank=True, null=True)
    birth = models.IntegerField(blank=True, null=True)
    death = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
#        b=self.birth if self.birth!=None else "####"
#        d=self.death if self.death!=None else "####"
#        return "{} {} ({}-{})".format(self.name, self.family_name, b, d)
        return "{} {}".format(self.name, self.family_name)

    class Meta:
        db_table = 'authors'
        ordering= ["name", "family_name", "birth"]
        managed=True

class Book(models.Model):
    id_books = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    valoration = models.IntegerField(blank=True, null=True)
    read_start = models.DateField(blank=True, null=True)
    read_end = models.DateField(blank=True, null=True)
    id_authors = models.ForeignKey(Author, models.DO_NOTHING, db_column='id_authors')
    
    def __str__(self):
        return "{} ({})".format(self.title, self.year)

    class Meta:
        db_table = 'books'
        ordering= ["title", "id_authors"]
        managed=True
