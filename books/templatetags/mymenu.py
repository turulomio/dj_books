from django import template
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
## El menu es un array del tipo
##Group1=[(Nivel, Nombre,[grupos],url),
## (Nivel, Nombre,[grupos],url),
## Group2
##]

class Action:
    def __init__(self,name,permissions,url):
        self.name=name
        self.permissions=permissions
        self.url=url

    def render(self):
       return """<li><a href="{}">{}</a></li>\n""".format(self.url,self.name)

## Can have actions or other menus
"""
<nav>
    <ul class="nav nav_level_1">
        <li><a href="database/">All database</a></li>
        <li><a href="#" class="toggle-custom" id="btn-1" data-toggle="collapse" data-size="small" data-target="#submenu1" aria-expanded="false">My Library...</a>
             <ul class="nav collapse nav_level_2" id="submenu1" role="menu" aria-labelledby="btn-1">
                  <li><a href="books/author/new/">Add author</a></li>
                  <li><a  href="books/book/new/">Add book</a></li>
                  <li><a href="#" class="toggle-custom" id="btn-3" data-toggle="collapse" data-target="#submenu3" aria-expanded="false">My valorations...</a>
                      <ul class="nav collapse nav_level_3" id="submenu3" role="menu" aria-labelledby="btn-3">
                          <li><a href="books/valoration/new/">Add a new valoration</a></li>
                          <li><a href="books/valoration/list/">Valoration list</a></li>
                      </ul>
                  </li>
             </ul>
        </li>
    </ul>
</nav>

"""


## Arr can be actions or a group object
class Group:
    def __init__(self,level,name,id,):
        self.arr=[]
        self.level=level
        self.name=name
        self.id=id
    
    def render(self):
        r="""<li><a href="#" class="toggle-custom" id="btn-{0}" data-toggle="collapse" data-target="#submenu{0}" aria-expanded="false">{1} ...</a>\n""".format(self.id,self.name)
        r=r+"""<ul class="nav collapse nav_level_{0}" id="submenu{1}" role="menu" aria-labelledby="btn-{1}">\n""".format(self.level+1,self.id)
        for item in self.arr:
            if item.__class__==Group:
                r=r+item.render()
            else:#Action
                r=r+item.render()
        r=r+"""</ul>\n"""
        r=r+"""</li>\n"""
        return r

    def append(self,o):
        self.arr.append(o)


class Menu:
    def __init__(self, user):
        self.arr=[]
        self.level=None
        self.user=user

    def render(self):
        r="<nav>\n"
        r=r+"""<ul class="nav nav_level_1">\n"""
        for item in self.arr:
            r=r+item.render()

        r=r+"""</ul>\n"""
        r=r+"</nav>\n"
        perm_list = self.user.user_permissions.all().values_list('codename', flat=True)
        r=r+"<p>"+ str(perm_list)
        return r

    def append(self,o):
        self.arr.append(o)
        
        

register = template.Library()


@register.simple_tag
def mymenu(user):
    menu=Menu(user)
    if user.is_authenticated:
        menu.append(Action(_("All database"),[], reverse_lazy("database")))
        grLibrary=Group(1,_("My Library"), "10")
        grLibrary.append(Action(_("Add author"),[], reverse_lazy("author-add")))
        grLibrary.append(Action(_("Add book"),[],reverse_lazy("book-add")))
        grVal=Group(2,_("My Valorations"), "11")
        grVal.append(Action(_("Add a valoration"),[], reverse_lazy("valoration-add")))
        grVal.append(Action(_("List of valorations"),[], reverse_lazy("valoration-list")))
        grLibrary.append(grVal)
        menu.append(grLibrary)
    return menu.render()

