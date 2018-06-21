"""dj_books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import reverse_lazy
#from django.conf import settings

from dj_books.views import  (
    home, 
    database,  
    profile_edit,  
    AuthorCreate,  
    AuthorDelete,  
    AuthorUpdate, 
    BookCreate, 
    BookUpdate, 
    BookDelete, 
    ValorationCreate, 
    ValorationUpdate, 
    ValorationDelete, 
    valoration,
    )

## Return a reg expression appending WWWSUBDIR, from absoluth
def ab(reg):
    return reg
    #return  r"{}{}{}".format(reg[:1], settings.WEBSUBDIR , reg[1:])

urlpatterns = [
    url(ab(r'^admin/'), admin.site.urls,  name="admin-site"),

#    url(ab(r'^admin/login/$'), RedirectView.as_view(url='/'), name="admin-login"),
#    url(r'^accounts/login/$', RedirectView.as_view(url='/')),
    url(ab(r'^accounts/login/$'), auth_views.login, {'template_name': 'admin/login.html'}, name="login"), 

    url(ab(r'^logout/$'), auth_views.logout, {'next_page': reverse_lazy('home')}, name="logout"), 
    url(ab(r'^$'), home, name='home'),
    url(ab(r'^database/$'), database, name='database'), 
    url(ab(r'^profile/$'), profile_edit, name="profile"), 

    url(ab(r'^books/author/new/$'), AuthorCreate.as_view(), name='author-add'),
    url(ab(r'^books/author/(?P<pk>\d+)/$'), AuthorUpdate.as_view(), name='author-edit'),
    url(ab(r'^books/author/(?P<pk>\d+)/delete/$'), AuthorDelete.as_view(), name='author-delete'),

    url(ab(r'^books/book/new/$'), BookCreate.as_view(), name='book-add'),
    url(ab(r'^books/book/(?P<pk>\d+)/$'), BookUpdate.as_view(), name='book-edit'),
    url(ab(r'^books/book/(?P<pk>\d+)/delete/$'), BookDelete.as_view(), name='book-delete'),

    url(ab(r'^books/valoration/list/'), valoration, name='valoration-list'),
    url(ab(r'^books/valoration/new/$'), ValorationCreate.as_view(), name='valoration-add'),
    url(ab(r'^books/valoration/(?P<pk>\d+)/$'), ValorationUpdate.as_view(), name='valoration-edit'),
    url(ab(r'^books/valoration/(?P<pk>\d+)/delete/$'), ValorationDelete.as_view(), name='valoration-delete'),
]

