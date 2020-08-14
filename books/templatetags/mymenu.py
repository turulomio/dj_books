from django import template
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
"""
    Esta clase la cree después de probar la app django-sitemaps, tenía cosas buenas, tree, breadcumb, title
    Era muy complicada y luego me liaba cuando el menu necesitaba parámetros
"""

class Action:
    ## @param name
    ## @param permissions. List of string if None is always showed
    def __init__(self,name,permissions,url):
        self.name=name
        self.permissions=permissions
        self.url=url

    def render(self, userpers, user, current_url_name):
        if self.__has_all_user_permissions(userpers) or user.is_superuser:
            if self.is_selected(current_url_name):
                return """<li class="Selected"><a class="Selected" href="{}">{}</a></li>\n""".format(reverse_lazy(self.url),self.name)
            else:
                return """<li><a href="{}">{}</a></li>\n""".format(reverse_lazy(self.url),self.name)
        else:
            return ""

    ## @return boolean if item is the selected one
    def is_selected(self, current_url_name):
        if current_url_name==self.url:
            return True
        return False
       
       
    def __has_all_user_permissions(self, userpers):
        if self.permissions is None:
            return True

        for p in self.permissions:
            if p not in userpers:
                return False
        return True

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
## No tiene permisos, busca en las acciones internas.
class Group:
    def __init__(self,level,name, id):
        self.arr=[]
        self.level=level
        self.name=name
        self.id=id
        
    ## Search for some permissions, not all
    def __user_has_some_children_permissions(self, userpers):
        for p in self.get_all_permissions():
            if p is None:
                return True
            if p in userpers:
                return True
        return False
        
    def get_all_permissions(self):        
        r=set()
        for item in self.arr:
            if item.__class__==Group:
                for p in item.get_all_permissions():
                    r.add(p)
            else:#Action
                if item.permissions is None:
                    r.add(None)
                    continue
                for p in item.permissions:
                    r.add(p)
        return r
    
    def render(self, userpers, user, current_url_name):
        r=""
        if self.__user_has_some_children_permissions(userpers) or user.is_superuser:
            collapsing="" if self.has_selected_actions(current_url_name) is True else "collapse"
            r=r+"""<li><a href="#" class="toggle-custom" id="btn-{0}" data-toggle="collapse" data-target="#submenu{0}" aria-expanded="false">{1} ...</a>\n""".format(self.id,self.name)
            r=r+"""<ul class="nav """+collapsing+""" nav_level_{0}" id="submenu{1}" role="menu" aria-labelledby="btn-{1}">\n""".format(self.level+1,self.id)
            for item in self.arr:
                if item.__class__==Group:
                    r=r+item.render(userpers, user,current_url_name)
                else:#Action
                    r=r+item.render(userpers, user, current_url_name)
            r=r+"""</ul>\n"""
            r=r+"""</li>\n"""
        return r

    def append(self,o):
        self.arr.append(o)

    def has_selected_actions(self,current_url_name):
        for item in self.arr:
            if item.__class__==Action:
                if item.is_selected(current_url_name) is True:
                    return True
            else: #Group
                return self.has_selected_actions(current_url_name)
        return False





class Menu:
    def __init__(self, appname):
        self.arr=[]
        self.appname=appname


    ## Renders an HTML menu
    ## @todo Leave selected current action
    def render_menu(self, user, current_url_name):
        r="<nav>\n"
        r=r+"""<ul class="nav nav_level_1">\n"""
        for item in self.arr:
            r=r+item.render(user.get_all_permissions(), user, current_url_name)#Inherited from group and from user)
        r=r+"""</ul>\n"""
        r=r+"</nav>\n"
        r=r+"<p>"
        return r

    ## Renders an HTML menu
    ## @todo Leave selected current action
    def render_pagetitle(self,current_url_name):
        action=self.find_action_by_url(current_url_name)
        action_name="None" if action is None else action.name
        return "{} > {}".format(self.appname, action_name)

    def append(self,o):
        self.arr.append(o)

    def find_action_by_url(self,url_name):
        for item in self.arr:
            if item.__class__==Group:
                for action in item.arr:
                    if action.url==url_name:
                        return action
            else:#Action
                if item.url==url_name:
                    return item
        return None

register = template.Library()


@register.simple_tag(takes_context=True)
def mymenu(context):
    user=context['user']
    url_name=context['request'].resolver_match.url_name
    return format_html(menu.render_menu(user,url_name))

@register.simple_tag(takes_context=True)
def mypagetitle(context):
    url_name=context['request'].resolver_match.url_name
    return  menu.render_pagetitle(url_name)


global menu    
menu=Menu(_("My Library"))
menu.append(Action(_("Search"), None,  "home"))

menu.append(Action(_("Add author"), ['books.add_author', ], "author-add"))

menu.append(Action(_("My valorations"), ['books.search_valoration'], "valoration-list"))

grQuerys=Group(1, _("Queries"), "12")
grQuerys.append(Action(_("Most valued books"), ['books.create_valoration', ], "query_books_valued"))
grQuerys.append(Action(_("Unfinished books"), ['books.create_valoration', ], "unfinished-books"))


grStatistics=Group(1, _("Statistics"), "13")
grStatistics.append(Action(_("Global"),['books.statistics_global',], "statistics-global"))
grStatistics.append(Action(_("User"),['books.statistics_user',], "statistics-user"))

menu.append(grQuerys)
menu.append(grStatistics)

