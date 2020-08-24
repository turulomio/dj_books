## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

#    Esta clase la cree después de probar la app django-sitemaps, tenía cosas buenas, tree, breadcumb, title
#    Era muy complicada y luego me liaba cuando el menu necesitaba parámetros

#    You need to create a menu in app.context_processor.py


from django import template
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

class Action:
    ## @param name
    ## @param permissions. List of string if None or [] is always showed
    ## @param authenticated Boolean. If True user needs to be logged
    def __init__(self,name,permissions,url,authenticated):
        self.name=name
        self.permissions=permissions
        self.url=url
        self.authenticated=authenticated

    def render(self, userpers, user, current_url_name):
        if self.__has_all_user_permissions(user, userpers):
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

    def __has_all_user_permissions(self, user, userpers):
        if user.is_superuser:
            return True

        if user.is_authenticated==self.authenticated:
            if self.permissions is None:
                return True

            for p in self.permissions:
                if p not in userpers:
                    return False
            return True
        else:
            return False

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
    def __init__(self,level,name, id, authenticated):
        self.arr=[]
        self.level=level
        self.name=name
        self.id=id
        self.authenticated=authenticated
        
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
        if (self.__user_has_some_children_permissions(userpers) and user.is_authenticated==self.authenticated) or user.is_superuser:
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
        if action is None:
            return self.appname
        else:
            return "{} > {}".format(self.appname, action.name)

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
    return format_html(context['menu'].render_menu(user,url_name))

@register.simple_tag(takes_context=True)
def mypagetitle(context):
    # return the version value as a dictionary
    # you may add other values here as well
    url_name=context['request'].resolver_match.url_name
    return  context['menu'].render_pagetitle(url_name)