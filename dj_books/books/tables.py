import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import Author, Book
from books.table_easy import TableFromModel

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
        
        
class TableEasyAuthors(TableFromModel):
    def __init__(self,  queryset):
        TableFromModel.__init__(self, Author,  queryset)
        self.setFields("id", ["name", "family_name", "birth", "death"])
