import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import Author, Book, Valoration
from books.table_easy import TableEasyFromModel

class AuthorTable(tables.Table):
    class Meta:
        model = Author
        template_name = 'django_tables2/table.html'
        exclude = ("id",)
        my_column = tables.TemplateColumn(verbose_name=_('My Column'), template_name="home.html")


class BookTable(tables.Table):
    class Meta:
        model = Book
        template_name = 'django_tables2/semantic.html'
        exclude = ("id",)
        
        
class TableEasyAuthors(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, Author,  queryset)
        self.setFields("id", ["name", "family_name", "birth", "death"])
        self.setIBM("/books/author/new/", "/books/author/###/", "/books/author/###/delete/")

class TableEasyBooks(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, Book,  queryset)
        self.setFields("id", ["title", "author", "year"])
        self.setIBM("/books/book/new/", "/books/book/###/", "/books/book/###/delete/")

class TableEasyValorations(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, Valoration,  queryset)
        self.setFields("id", ["book", "read_start", "read_end", "valoration"])
        self.setIBM("/books/valoration/new/", "/books/valoration/###/", "/books/valoration/###/delete/")
