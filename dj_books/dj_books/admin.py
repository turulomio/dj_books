## @package admin
## @brief Defines everything for Django Admin Site

## Se mete en books  porque necesita los modelos


from django.utils.translation import ugettext_lazy
from books.models import  Profile
from django.contrib.auth.models import Permission,  Group, User
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy
from django.contrib import admin# Need to import this since auth models get registered on import.

admin.site.unregister(User)
admin.site.unregister(Group)
## Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('My personal Django')

## Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('My personal Django')

## Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('My personal Django administration')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    

class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    list_display = ['name','content_type','codename']
    search_fields = ['name', 'content_type','codename']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group)
    
admin.site.site_url = reverse_lazy('home') 
admin.site.logout_template='admin/login.html'


#Removes default delete_selected action
admin.site.disable_action('delete_selected')
