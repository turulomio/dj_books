from django import template
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

class Action:
    def __init__(self,name,permissions,url):
        self.name=name
        self.permissions=permissions
        self.url=url

    def render(self, userpers):
        if self.__has_all_user_permissions(userpers) or userpers.is_superuser():
            return """<li><a href="{}">{}</a></li>\n""".format(self.url,self.name)
        else:
            return ""
       
       
    def __has_all_user_permissions(self, userpers):
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
                for p in item.permissions:
                    r.add(p)
        return r
    
    def render(self, userpers):
        r=""
        #        print("Group render", self.get_all_permissions(), userpers, self.__user_has_some_children_permissions(userpers))
        if self.__user_has_some_children_permissions(userpers) or userpers.is_superuser():
            r=r+"""<li><a href="#" class="toggle-custom" id="btn-{0}" data-toggle="collapse" data-target="#submenu{0}" aria-expanded="false">{1} ...</a>\n""".format(self.id,self.name)
            r=r+"""<ul class="nav collapse nav_level_{0}" id="submenu{1}" role="menu" aria-labelledby="btn-{1}">\n""".format(self.level+1,self.id)
            for item in self.arr:
                if item.__class__==Group:
                    r=r+item.render(userpers)
                else:#Action
                    r=r+item.render(userpers)
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


    ## Renders an HTML menu
    ## @todo Leave selected current action
    def render(self):
        r="<nav>\n"
        r=r+"""<ul class="nav nav_level_1">\n"""
        for item in self.arr:
            r=r+item.render(self.user.get_all_permissions())#Inherited from group and from user)
        r=r+"""</ul>\n"""
        r=r+"</nav>\n"
        r=r+"<p>"
        return r
    

    def append(self,o):
        self.arr.append(o)
        
        

register = template.Library()


@register.simple_tag
def mymenu(user):
    """
        books.change_valoration
        books.add_valoration
        books.change_author
        books.add_book
        books.delete_book
        books.change_book
        books.delete_valoration
        books.delete_author
        books.add_author
    """
    menu=Menu(user)
    menu.append(Action(_("All database"),['books.search_author', 'books.search_book'],  reverse_lazy("database")))
    grLibrary=Group(1,_("My Library"),"10")
    grLibrary.append(Action(_("Add author"),['books.add_author', ], reverse_lazy("author-add")))
    grLibrary.append(Action(_("Add book"),['books.add_book', ],reverse_lazy("book-add")))
    grVal=Group(2,_("My Valorations"), "11")
    grVal.append(Action(_("Add a valoration"),['books.add_valoration'], reverse_lazy("valoration-add")))
    grVal.append(Action(_("List of valorations"),['books.search_valoration'], reverse_lazy("valoration-list")))
    grLibrary.append(grVal)

    grQuerys=Group(1, _("Queries"), "12")
    grQuerys.append(Action(_("Last books"),['books.search_author','books.search_book'], reverse_lazy("query-books-last")))
    grQuerys.append(Action(_("Most valued books"),['books.search_author','books.search_book'], reverse_lazy("query-books-valued")))
    
    
    grQuerys=Group(1, _("Statistics"), "13")
    grQuerys.append(Action(_("Global"),['books.statistics_global',], reverse_lazy("statistics")))
    grQuerys.append(Action(_("User"),['books.statistics_user',], reverse_lazy("statistics")))
    menu.append(grLibrary)
    menu.append(grQuerys)
    return menu.render()

