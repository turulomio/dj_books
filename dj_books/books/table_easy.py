from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _

## Class to store an url and associated permissions. Permissions is an array
class UrlAccess:
    def __init__(self):
        self.url=None
        self.permissions=[]
        self.visible=False
    
    def isSet(self):
        if self.url!=None:
            return True
        return False
        
    def set(self, url, permissions, visible):
        self.url=url
        self.permissions=permissions
        self.visible=visible


class TableEasy(ABC):
    def __init__(self, name):
        self._width="100%"
        self._height="100%"
        self.setName(name)
        self._selectable=False
        self.create=UrlAccess()
        self.read=UrlAccess()
        self.update=UrlAccess()
        self.delete=UrlAccess()
        self.export=UrlAccess()


    ## Returns if all urls and buttons are invisible
    def allInvisible(self):
        if self.create.visible==False and self.read.visible==False and self.update.visible==False and self.delete.visible==False and self.export.visible==False:
            return True
        return False
    def selectable(self):
        return self._selectable
        
    ## Sets if checkbox are shwon
    def setSelectable(self, boolean):
        self._selectable=boolean

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

        
    ## CRUDE Create, Read, Update, Delete, Export
    ## url es url, per permissions, vis, visibility
    ## Permissions is an array
    def setCRUDE(self, c_url, c_per, c_vis, r_url, r_per, r_vis,  u_url, u_per, u_vis,  d_url, d_per, d_vis,  e_url, e_per,  e_vis):
        self.create.set(c_url, c_per, c_vis)
        self.read.set(r_url, r_per, r_vis)
        self.update.set(u_url, u_per, u_vis)
        self.delete.set(d_url, d_per,  d_vis)
        self.export.set(e_url, e_per,  e_vis)
        
    ## @todo Function that overrides visibility and sets visibility with permissions
    def setVisibilityWithPermissions(self, userpers):
        pass

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
        if len(self.queryset)==0:
            return _("No records found")
        r='<div class="TableEasyDiv" id="{}">\n'.format(self.name())
        ##Search box
        r=r+"""<div class="input-group"><span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span><input  class="form-control TableEasySearch" type="text" id="{0}_search" onkeyup="TableEasy_search_onkeyup('{0}')" placeholder="Search for names..." title="Type in a name"></div>\n""".format(self.name())
        r=r+'<table class="TableEasy" id="{}_table">\n'.format(self.name())
        r=r+'<tr class="header">\n'
        ##Header1
        if self.selectable():
            r=r+"""<th><input type="checkbox" id="{0}_chkAll" class="TableEasyCheckBoxAll" onclick="TableEasy_chkAll_onclick('{0}');" /></th>\n""".format(self.name())
        for header in self.headers:
            r=r+"""<th>{}</th>\n""".format(header)
        if self.allInvisible()==False:
            r=r+'<th>{}</th>\n'.format(_("Actions"))
        r=r+"        </tr>\n"
        ##Data
        for row in self.queryset:
            pk_id=self.getValue_from_string_field(row, self.string_fields_pk)
            r=r+"""<tr class="data">\n"""
            if self.selectable():
                r=r+'<td><input type="checkbox" class="TableEasyCheckBox" id="{0}_{1}" /></td>\n'.format(self.name(),pk_id)
            for sf in self.string_fields:
                value=self.getValue_from_string_field(row, sf)
                if value==None:
                    value ="- "
                if value.__class__ in (float, int) or value=="- ":
                    r=r+"""<td style="text-align: right;">{}</td>\n""".format(value)
                else:
                    r=r+"""<td>{}</td>\n""".format(value)
            if self.allInvisible()==False:
                r=r+"""<td>\n"""
                if self.update.visible:
                    r=r+"""<button type="button" class="btn btn-default" name="cmd_update"  onclick="window.location.href='{}';"><span class="glyphicon glyphicon-edit"></span></button>""".format(self.update.url.replace("###",str(pk_id)))
                if self.delete.visible:
                    r=r+"""<button type="button" class="btn btn-default" name="cmd_delete"  onclick="window.location.href='{}';"><span class="glyphicon glyphicon-remove"></span></button>""".format(self.delete.url.replace("###",str(pk_id)))
                r=r+"""</td>\n"""
            r=r+"        </tr>\n"
        r=r+"    </table>\n"
        if self.create.visible:
            r=r+"""<button type="button" class="btn btn-default" name="cmd_insert" onclick="window.location.href='{}';" ><span class="glyphicon glyphicon-plus"></span></button>\n""".format(self.create.url)
        if self.selectable() and self.delete.visible:
            r=r+"""<button type="button" class="btn btn-default" name="cmd_delete_selected" onclick="window.location.href='{}';" ><span class="glyphicon glyphicon-remove-circle"></span></button>\n""".format(self.delete.url, _("Delete selected"))
        if self.export.visible:
            r=r+"""<button type="button" class="btn btn-default" name="cmd_export"  onclick="window.location.href='{}';"><span class="glyphicon glyphicon-export"></span></button>""".format(self.export.url.replace("###",str(pk_id)))

        r=r+"""<label class="TableEasyRecords" id="{}_records">""".format(self.name()) + _("Found {} records").format(len(self.queryset)) + """</label>\n"""
        r=r+"</div>\n"
        return r
        
def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    from django.http import HttpResponse
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([smart_str(u"ID"), smart_str(u"Title"), smart_str(u"Description"),])
    for obj in queryset:
        writer.writerow([ smart_str(obj.pk), smart_str(obj.title), smart_str(obj.description), ])
    return response
    export_csv.short_description = u"Export CSV"
