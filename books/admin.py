from django.contrib import admin
from dj_books.admin import mysite
from django.contrib.auth.models import Permission,  Group, User
from .models import Author, Book,  Profile
from django.contrib.auth.admin import UserAdmin

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_name', 'birth', 'death')
    search_fields = ('name', 'family_name', 'birth', 'death')
    list_filter = ('birth','death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'author','year')
    search_fields = ('title',   )
    list_filter = ('author','year')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


mysite.register(User, CustomUserAdmin)
mysite.register(Group)
mysite.register(Permission)
mysite.register(Author, AuthorAdmin)
mysite.register(Book, BookAdmin)
mysite.logout_template='admin/login.html'
mysite.site_url ="/home"

#Removes default delete_selected action
mysite.disable_action('delete_selected')
