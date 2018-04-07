import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import Author, Book

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