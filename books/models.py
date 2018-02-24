# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#from __future__ import unicode_literals
from  django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'profiles'
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Author(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_authors")
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
    id = models.AutoField(primary_key=True, db_column="id_books")
    title = models.TextField(null=False)
    year = models.IntegerField(null=True)
    author = models.ForeignKey(Author, models.DO_NOTHING, db_column='id_authors')
    
    def __str__(self):
        return "{} ({})".format(self.title, self.year)

    class Meta:
        db_table = 'books'
        ordering= ["title", "author"]
        managed=True

class Valoration(models.Model):
    id=models.AutoField(primary_key=True, db_column="id")
    book = models.ForeignKey(Book,  models.DO_NOTHING, db_column="id_books")
    user = models.ForeignKey(User)
    comment = models.TextField(blank=True, null=True)
    valoration = models.IntegerField(blank=True, null=True)
    read_start = models.DateField(blank=True, null=True)
    read_end = models.DateField(blank=True, null=True)
        
    def __str__(self):
        return "Valoration of {} ({})".format(self.id_books, self.user.name)

    class Meta:
        db_table = 'valorations'
        ordering= ["valoration","read_end"]
        managed=True
        
class FileBooks(models.Model):
    id=models.AutoField(primary_key=True)
    book = models.ForeignKey(Book,  models.DO_NOTHING, db_column="id_books")
    PDF= 'PDF'
    ODT= 'ODT'
    DOC="DOC"
    DOCX="DOCX"
    EPUB="EPUB"
    MOBI="MOBI"
    FORMATS= (
        (PDF, 'PDF'),
        (ODT, 'ODT'),
        (DOCX, 'DOCX'),
        (EPUB, 'EPUB'),
        (MOBI, 'MOBI'),
        (DOC, 'DOC')
    )
    formats= models.CharField(
        max_length=4,
        choices=FORMATS,
        default=ODT,
    )
    
