## @package admin
## @brief Defines everything for Django Admin Site

## Se mete en books  porque necesita los modelos


from books.models import Author, Book,  Valoration
from django.contrib import admin# Need to import this since auth models get registered on import.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_name', 'birth', 'death')
    search_fields = ('name', 'family_name', 'birth', 'death')
    list_filter = ('birth','death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'author','year')
    search_fields = ('title',   )
    list_filter = ('author','year')
    
class ValorationAdmin(admin.ModelAdmin):
    list_display = ('comment',  'read_start','read_end',  'valoration', 'book', 'user')
    search_fields = ('comment',  'read_start','read_end',  'valoration', 'book')
    list_filter = ('user','read_start', 'read_end')



admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Valoration, ValorationAdmin)
