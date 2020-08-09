# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#from __future__ import unicode_literals
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):    
    SPANISH= 'ES'
    ENGLISH = 'EN'
    FRENCH="FR"
    LANGUAGES= (
        (SPANISH, 'Español'),
        (ENGLISH, 'English'),
        (FRENCH, 'Francés')
    )
    language= models.CharField(max_length=2, choices=LANGUAGES, default=ENGLISH, verbose_name=_("Language"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth date"))
    email_confirmed = models.BooleanField(default=False)
    class Meta:
        db_table = 'profiles'
        permissions=(
            ("statistics_global",  "Can see global statistics"), 
            ("statistics_user",  "Can see user statistics"), 
            ('search_book', 'Can search books'), 
            ('search_author', 'Can search authors'), 
            ('search_valoration', 'Can search valorations'), 
            ('database_all_view', 'Can see a view with all database'), 
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Author(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_authors")
    name = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Name"))
    family_name = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Family name"))
    birth = models.IntegerField(blank=True, null=True, verbose_name=_("Birth year"))
    death = models.IntegerField(blank=True, null=True, verbose_name=_("Death year"))
    
    GENDER=(
        (0,  _("Man")), 
        (1,  _("Woman"))
        )

    gender= models.IntegerField(choices=GENDER, default=0,  verbose_name=_("Gender"))

    def __str__(self):
        b=self.birth if self.birth!=None else "####"
        d=self.death if self.death!=None else "####"
        return "{} {} ({}-{})".format(self.name, self.family_name, b, d)

    def full_name(self):
        """
           Returns full name of the Author
        """
        if self.name==None and self.family_name==None:
            return ""
        elif self.name==None and self.family_name!=None:
            return self.family_name
        elif self.name!=None and self.family_name==None:
            return self.name
        elif self.name!=None and self.family_name!=None:
            return "{} {}".format(self.name,self.family_name)

    def lifetime_string(self):
        if self.birth is None:
            return ""
        if self.death is None:
            return _("{}-").format(self.birth)
        else:
            return "{}-{}".format(self.birth, self.death)

    def age_string(self):
        if self.birth is None:
            return ""
        if self.death is None:
            return _("{} years").format(date.today().year-self.birth)
        else:
            return _("Lived {} years").format(self.death-self.birth)

    class Meta:
        db_table = 'authors'
        ordering= ["name", "family_name", "birth", "death", "gender"]
        managed=True

## Class that manages Book database model
class Book(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_books")
    title = models.CharField(max_length=100,null=False, verbose_name=_("Title"))
    year = models.IntegerField(blank=True, null=True, verbose_name=_("Year"))
    author = models.ForeignKey(Author, models.DO_NOTHING, db_column='id_authors', blank=False, null=False)

    def __str__(self):
        return "{} ({})".format(self.title, self.year)

    class Meta:
        db_table = 'books'
        ordering= ["title", "author"]
        managed=True

    ## @todo
    ## Make a function to resume valorations. It must be showed in Book Model
    ## @endtodo
    def valorations(self):
        pass

class Valoration(models.Model):
    id=models.AutoField(primary_key=True, db_column="id")
    book = models.ForeignKey(Book,  models.DO_NOTHING, db_column="id_books", verbose_name=_("Book"))
    user = models.ForeignKey(User, models.DO_NOTHING)
    comment = models.TextField(blank=True, null=True)
    valoration = models.IntegerField(blank=True, null=True, verbose_name="Valoration [0-100]", validators=[MaxValueValidator(100),MinValueValidator(0)])
    read_start = models.DateField(blank=True, null=True,verbose_name="Date read started")
    read_end = models.DateField(blank=True, null=True,verbose_name="Date read ended")

    def __str__(self):
        return _("Valoration of {} ({}) by {}: {}").format(self.book.title, self.book.author.full_name(), self.user.email, self.valoration)
    ## Days took read
    ## @return int Number of days
    def read_took(self):
        return (self.read_end -self.read_start).days

    class Meta:
        db_table = 'valorations'
        ordering= ["valoration","read_end","read_start"]
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


