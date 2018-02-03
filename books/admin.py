from django.contrib import admin


from django.contrib.auth.models import Permission
admin.site.register(Permission)


# Register your models here.
from .models import Author, Book

admin.site.register(Author)
admin.site.register(Book)

#Removes default delete_selected action
admin.site.disable_action('delete_selected')
