from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _
class TableEasy(ABC):
    def __init__(self, name):
        self._width="100%"
        self._height="100%"
        self._html_delete=""
        self._html_insert=""
        self._html_update=""
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
        
    ## Puede haber un punto
    def setFields(self, string_fields_pk, string_fields):
        self.string_fields=string_fields
        self.string_fields_pk=string_fields_pk
        self.headers=[]
        for sf in string_fields:
            self.headers.append(self.getHeader_from_string_field(sf))

        
    def setIBM(self, html_insert, html_update, html_delete):
        self._html_insert=html_insert
        self._html_update=html_update
        self._html_delete=html_delete

    def setName(self, name):
        self._name=name

    def name(self):
        return self._name
        
    ##Object can be
    ## - django.db.models.fields.related_descriptors.ForwardManyToOneDescriptor
    ## - django.db.models.query_utils.DeferredAttribute 
    def headerName(self, field):
        a=field.split(".")
        if len(a)==1:
            return field.verbose_name
        elif len(a)==2:
            return "Nose"
            object2=getattr(object, a[0])
            return getattr(object2, a[1])

            
        
    ## s, si es una valoration pede ser start_read
    ## s, si quiero sacar un titulo del libro puede ser book.title
    ## row es un objeto como Valoration de un queryset
    def getValue_from_string_field(self, row, sf):
        a=sf.split(".")
        if len(a)==1:
            return getattr(row, sf)
        elif len(a)==2:
            object2=getattr(row, a[0])
            return getattr(object2, a[1])

    def getHeader_from_string_field(self, sf):
            a=sf.split(".")
            if len(a)==1:
                return self.queryset.model._meta.get_field(sf).verbose_name
            if len(a)==2:#book.valoration coge el book
                return sf
##getattr(o, field.name, None)
class TableEasyFromModel(TableEasy):
    def __init__(self, name, model, queryset):
        TableEasy.__init__(self, name)
        self.model=model
        self.queryset=queryset

    def html_with_pk(self, html):
        return html.replace("###",self.fields_pk)

    
    def render(self):
        r='<div class="TableEasyDiv" id="{}">\n'.format(self.name())
        ##Search box
        r=r+"""<div class="input-group"><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span><input  class="form-control TableEasySearch" type="text" id="{0}_search" onkeyup="TableEasy_search_onkeyup('{0}')" placeholder="Search for names..." title="Type in a name"></div>\n""".format(self.name())
        r=r+'<table class="TableEasy" id="{}_table">\n'.format(self.name())
        r=r+'<tr class="header">\n'
        ##Header1
        r=r+"""<th><input type="checkbox" id="{0}_chkAll" class="TableEasyCheckBoxAll" onclick="TableEasy_chkAll_onclick('{0}');" /></th>\n""".format(self.name())
        for header in self.headers:
            r=r+"""<th>{}</th>\n""".format(header)
        r=r+'<th>{}</th>\n'.format(_("Actions"))
        r=r+"        </tr>\n"
        ##Data
        for row in self.queryset:
            pk_id=self.getValue_from_string_field(row, self.string_fields_pk)
            r=r+"""<tr class="data">\n"""
            r=r+'<td><input type="checkbox" class="TableEasyCheckBox" id="{0}_{1}" /></td>\n'.format(self.name(),pk_id)
            for sf in self.string_fields:
                value=self.getValue_from_string_field(row, sf)
                if value==None:
                    value ="- "
                if value.__class__ in (float, int) or value=="- ":
                    r=r+"""<td style="text-align: right;">{}</td>\n""".format(value)
                else:
                    r=r+"""<td>{}</td>\n""".format(value)
            r=r+"""<td><button type="button" class="TableEasyButton" name="cmd_update"  onclick="window.location.href='{}';">{}</button>""".format(self._html_update.replace("###",str(pk_id)), _("Update"))
            r=r+"""<button type="button" class="TableEasyButton" name="cmd_delete"  onclick="window.location.href='{}';">{}</button></td>\n""".format(self._html_delete.replace("###",str(pk_id)), _("Delete"))
            r=r+"        </tr>\n"
        r=r+"    </table>\n"
        r=r+"""<button type="button" class="TableEasyButton" name="cmd_insert" onclick="window.location.href='{}';" ><span class="glyphicon glyphicon-plus"></span>{}</button>\n""".format(self._html_insert, _("Insert"))
        r=r+"""<button type="button" class="TableEasyButton" name="cmd_delete_selected" onclick="window.location.href='{}';" >{}</button>\n""".format(self._html_insert, _("Delete selected"))
        r=r+"""<label class="TableEasyRecords" id="{}_records">""".format(self.name()) + _("Found {} records").format(len(self.queryset)) + """</label>\n"""
        r=r+"</div>\n"
        return r