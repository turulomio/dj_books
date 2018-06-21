from .models import Author, Book, Valoration
from books.table_easy import TableEasyFromModel
from django.utils.translation import gettext_lazy as _

class TableEasyAuthors(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyAuthor", Author,  queryset)
        self.setFields("id", ["name", "family_name", "birth", "death"])
        self.setCRUDE(  "/books/author/create/",  [], True, 
                                    "/books/author/###/", [], True,
                                    "/books/author/###/update/", [], True,
                                    "/books/author/###/delete/",[],True,
                                    "/books/author/export/",[],  True,)
                                    
        self.setSelectable(True)

class TableEasyBooks(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyBooks", Book,  queryset)
        self.setFields("id", ["title", "author", "year"])
        self.setCRUDE(  "/books/book/create/", [],False,
                                    "/books/book/###/", [],False,
                                    "/books/book/###/update/", [], False,
                                    "/books/book/###/delete/",[],False,
                                    "",[], False,)

class TableEasyValorations(TableEasyFromModel):
    def __init__(self,  queryset):
        TableEasyFromModel.__init__(self, "TableEasyValorations", Valoration,  queryset)
        self.setFields("id", ["book.title", "read_start", "read_end", "valoration","user.email", "comment"])
        self.setCRUDE(  "/books/valoration/create/", [], False,
                                    "/books/valoration/###/", [], False,
                                    "/books/valoration/###/update/", [], False, 
                                    "/books/valoration/###/delete/", [], False,
                                    "", [], False,)
        self.headers[0]=_("Book title")
        self.headers[4]=_("User mail")
