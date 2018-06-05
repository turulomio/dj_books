from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
class TableEasy(ABC):
    def __init__(self, name):
        self._width="100%"
        self._height="100%"
        self._html_delete=""
        self._html_insert=""
        self._html_update=""
        self._fields=[]
        self.setName(name)

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
        self._html_insert=html_insert
        self._html_update=html_update
        self._html_delete=html_delete

    def setName(self, name):
        self._name=name

    def name(self):
        return self._name

class TableEasyFromModel(TableEasy):
    def __init__(self, name, model, queryset):
        TableEasy.__init__(self, name)
        self.model=model
        self.queryset=queryset

    def html_with_pk(self, html):
        return html.replace("###",self.fields_pk)
        
    
    def render(self):
        print(self.name())
        r='<div class="TableEasyDiv" id="{}">\n'.format(self.name())
        ##Search box
        r=r+"""<div class="input-group"><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span><input  class="form-control TableEasySearch" type="text" id="{0}_search" onkeyup="TableEasy_search_onkeyup('{0}')" placeholder="Search for names..." title="Type in a name"></div>\n""".format(self.name())
        r=r+'<table class="TableEasy" id="{}_table">\n'.format(self.name())
        r=r+'<tr class="header">\n'
        ##Header1
        r=r+"""<th><input type="checkbox" id="{0}_chkAll" class="TableEasyCheckBoxAll" onclick="TableEasy_chkAll_onclick('{0}');" /></th>\n""".format(self.name())
        for field in self.fields:
            r=r+"<th>{}</th>\n".format(field.verbose_name)
        r=r+'<th>{}</th>\n'.format(_("Actions"))
        r=r+"        </tr>\n"
        ##Data
        for o in self.queryset:
            pk_id=getattr(o, self.fields_pk.name, None)
            r=r+"""<tr class="data">\n"""
            r=r+'<td><input type="checkbox" class="TableEasyCheckBox" id="{0}_{1}" /></td>\n'.format(self.name(),pk_id)
            for field in self.fields:
                r=r+"<td>{}</td>\n".format(getattr(o, field.name, None)) 
            r=r+"""<td><button type="button" class="TableEasyButton" name="cmd_update"  onclick="window.location.href='{}';">{}</button>""".format(self._html_update.replace("###",str(pk_id)), _("Update"))
            r=r+"""<button type="button" class="TableEasyButton" name="cmd_delete"  onclick="window.location.href='{}';">{}</button></td>\n""".format(self._html_delete.replace("###",str(pk_id)), _("Delete"))
            r=r+"        </tr>\n"
        r=r+"    </table>\n"
        r=r+"""<button type="button" class="TableEasyButton" name="cmd_insert" onclick="window.location.href='{}';" ><span class="glyphicon glyphicon-plus"></span>{}</button>\n""".format(self._html_insert, _("Insert"))
        r=r+"""<button type="button" class="TableEasyButton" name="cmd_delete_selected" onclick="window.location.href='{}';" >{}</button>\n""".format(self._html_insert, _("Delete selected"))
        r=r+"""<label class="TableEasyRecords" id="{}_records">""".format(self.name()) + _("Found {} records").format(len(self.queryset)) + """</label>\n"""
        r=r+"</div>\n"
        return r

def mymenu():
   menu=Menu()
   menu.append(Action(_("All database"),[],"/database/"))
   grLibrary=Group(1,_("My Library"), "10")
   grLibrary.append(Action(_("Add author"),[],"/books/author/new/"))
   grLibrary.append(Action(_("Add book"),[],"/books/book/new/"))
   grVal=Group(1,_("My Valorations"), "11")
   grVal.append(Action(_("Add a valoration"),[],"/books/valoration/new/"))
   grVal.append(Action(_("List of valorations"),[],"/books/valoration/list/"))
   grLibrary.append(grVal)
   menu.append(grLibrary)
   return menu