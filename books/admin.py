from django.contrib import admin
from dj_books.admin import mysite
from django.contrib.auth.models import Permission,  User,  Group
mysite.register(User)
mysite.register(Group)
mysite.register(Permission)
mysite.site_url ="/home"

# Register your models here.
from .models import Author, Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_name', 'birth', 'death')
    search_fields = ('name', 'family_name', 'birth', 'death')
    list_filter = ('birth','death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'id_authors','year','valoration')
    search_fields = ('title',  )
    list_filter = ('id_authors','year', 'valoration')

mysite.register(Author, AuthorAdmin)
mysite.register(Book, BookAdmin)

#Removes default delete_selected action
mysite.disable_action('delete_selected')
