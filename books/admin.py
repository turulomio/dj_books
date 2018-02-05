from django.contrib import admin
from dj_books.admin import mysite
from django.contrib.auth.models import Permission,  Group, User
from .models import Author, Book,  Profile
#from django.contrib.auth.admin import UserAdmin
#from .models import MyUser

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_name', 'birth', 'death')
    search_fields = ('name', 'family_name', 'birth', 'death')
    list_filter = ('birth','death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'id_authors','year','valoration')
    search_fields = ('title',  )
    list_filter = ('id_authors','year', 'valoration')

mysite.register(User)
mysite.register(Profile)
mysite.register(Group)
mysite.register(Permission)
mysite.register(Author, AuthorAdmin)
mysite.register(Book, BookAdmin)

mysite.site_url ="/home"

#Removes default delete_selected action
mysite.disable_action('delete_selected')
