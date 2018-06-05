from .models import Author, Book, Valoration
from books.table_easy import TableEasyFromModel
from django.utils.translation import gettext_lazy as _

class TableEasyAuthors(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyAuthor", Author,  queryset)
        print(self.name())
        self.setFields("id", ["name", "family_name", "birth", "death"])
        self.setIBM("/books/author/new/", "/books/author/###/", "/books/author/###/delete/")

class TableEasyBooks(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyBooks", Book,  queryset)
        self.setFields("id", ["title", "author", "year"])
        self.setIBM("/books/book/new/", "/books/book/###/", "/books/book/###/delete/")

class TableEasyValorations(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyValorations", Valoration,  queryset)
        self.setFields("id", ["book.title", "read_start", "read_end", "valoration","user.email"])
        self.setIBM("/books/valoration/new/", "/books/valoration/###/", "/books/valoration/###/delete/")
        self.headers[0]=_("Book title")
        self.headers[4]=_("User mail")
