from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
class Table(ABC):
    def __init__(self):
        self._width="100%"
        self._height="100%"
        self._delete_html=""
        self.i_nsert_html=""
        self._edit_html=""
        self._fields=[]
        self._name="table_easy"

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        

    @abstractmethod
    def render(self):
        return 
        
    def setFields(self, string_fields_pk, string_fields):
        self.fields=[]
        for field in string_fields:
            self.fields.append(self.model._meta.get_field(field))
        self.fields_pk=self.model._meta.get_field(string_fields_pk)
        
    def setIBM(self, html_insert, html_update, html_delete):
        pass

        
class TableFromModel(Table):
    def __init__(self, model, queryset):
        Table.__init__(self)
        self.model=model
        self.queryset=queryset
    
    def render(self):
        r='<div class="EasyTable">'
        ##Search box
        r=r+'<button type="button" name="cmd_insert">{}</button>'.format(_("Insert"))
        r=r+'<button type="button" name="cmd_insert">{}</button>'.format(_("Update"))
        r=r+'<button type="button" name="cmd_insert">{}</button>'.format(_("Delete"))
        r=r+'    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names.." title="Type in a name">\n'
        r=r+'<table id="myTable">\n'
        r=r+'<tr class="header">\n'
        ##Header
        r=r+'<td><input type="checkbox" id="all"/></td>\n'
        for field in self.fields:
            r=r+"<th>{}</th>\n".format(field.verbose_name)
        r=r+"        </tr>\n"
        ##Data
        r=r+'        <tr>\n'
        for o in self.queryset:
            r=r+"        <tr>\n"
            r=r+'<td><input type="checkbox" id="{}"/></td>\n'.format(getattr(o, self.fields_pk.name, None)) 
            for field in self.fields:
                r=r+"<td>{}</td>\n".format(getattr(o, field.name, None)) 
            r=r+"        </tr>\n"
        r=r+"    </table>\n"
        r=r+"</div>\n"
        return r
    
class TableFromQuerySet():
    def __init__(self):
        Table.__init__(self)








