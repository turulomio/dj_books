from .models import Author, Book, Valoration
from books.table_easy import TableEasyFromModel
from django.utils.translation import gettext_lazy as _

class TableEasyAuthors(TableEasyFromModel):
    def __init__(self,  queryset, request):
        TableEasyFromModel.__init__(self, "TableEasyAuthor", Author,  queryset, request)
        self.setFields("id", ["name", "family_name", "birth", "death"])
        self.setCRUDE(  "/books/author/create/",  ['books.add_author'],
                                    "/books/author/###/", ['books.search_author'],
                                    "/books/author/###/update/", ['books.change_author'],
                                    "/books/author/###/delete/",['books.delete_author'],
                                    "/books/author/export/",['books.export_author'] )
                                    
        self.setSelectable(True)

class TableEasyBooks(TableEasyFromModel):
    def __init__(self,  queryset, request):
        TableEasyFromModel.__init__(self, "TableEasyBooks", Book,  queryset, request)
        self.setFields("id", ["title", "author", "year"])
        self.setCRUDE(  "/books/book/create/", ['books.add_book'],
                                    "/books/book/###/", ['books.search_book'],
                                    "/books/book/###/update/", ['books.change_book'], 
                                    "/books/book/###/delete/",['books.delete_book'],
                                    "",['books.export_book'] )

class TableEasyValorations(TableEasyFromModel):
    def __init__(self,  queryset,  request):
        TableEasyFromModel.__init__(self, "TableEasyValorations", Valoration,  queryset, request)
        self.setFields("id", ["book.title", "read_start", "read_end", "valoration","user.email", "comment"])
        self.setCRUDE(  "/books/valoration/create/", ['books.add_valoration'], 
                                    "/books/valoration/read/###/", ['books.search_valoration'], 
                                    "/books/valoration/update/###/", ['books.change_valoration'],  
                                    "/books/valoration/delete/###/", ['books.delete_valoration'], 
                                    "", ['books.export_valoration'] )
        self.headers[0]=_("Book title")
        self.headers[4]=_("User mail")
