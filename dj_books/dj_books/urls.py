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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login, {'template_name': 'admin/login.html'}), 
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}), 
    url(r'^home/$', home, name='home'),
    url(r'^database/$', database, name='database'), 
    url(r'^profile/$', profile_edit), 

    url(r'^books/author/new/$', AuthorCreate.as_view(), name='author-add'),
    url(r'^books/author/(?P<pk>\d+)/$', AuthorUpdate.as_view(), name='author-edit'),
    url(r'^books/author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author-delete'),

    url(r'^books/book/new/$', BookCreate.as_view(), name='book-add'),
    url(r'^books/book/(?P<pk>\d+)/$', BookUpdate.as_view(), name='book-edit'),
    url(r'^books/book/(?P<pk>\d+)/delete/$', BookDelete.as_view(), name='book-delete'),

    url(r'^books/valoration/list/', valoration, name='valoration-list'),
    url(r'^books/valoration/new/$', ValorationCreate.as_view(), name='valoration-add'),
    url(r'^books/valoration/(?P<pk>\d+)/$', ValorationUpdate.as_view(), name='valoration-edit'),
    url(r'^books/valoration/(?P<pk>\d+)/delete/$', ValorationDelete.as_view(), name='valoration-delete'),
]

