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
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import reverse_lazy, include, path

## @todo Change views import to a generic way
from . import views as dj_books_views
from books import views as books_view

urlpatterns = [
    url(r'^signup/$', dj_books_views.signup, name='signup'),
    
    
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    url(r'^account_activation_sent/$', dj_books_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  dj_books_views.activate, name='activate'),
    
    url(r'^admin/', admin.site.urls,  name="admin-site"),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name="login"), 
#    url(r'^logout/$', auth_views.logout, {'next_page': reverse_lazy('home')}, name="logout"), 
    url(r'^$', books_view.home, name='home'),
    url(r'^database/$', books_view.database, name='database'), 
    url(r'^profile/$', dj_books_views.profile_edit, name="profile"), 

    url(r'^books/author/create/$', books_view.AuthorCreate.as_view(), name='author-add'),
    url(r'^books/author/(?P<pk>\d+)/$', books_view.author_read, name='author-read'), 
    url(r'^books/author/(?P<pk>\d+)/update/$', books_view.AuthorUpdate.as_view(), name='author-edit'),
    url(r'^books/author/(?P<pk>\d+)/delete/$', books_view.AuthorDelete.as_view(), name='author-delete'),

    url(r'^books/book/create/$', books_view.BookCreate.as_view(), name='book-add'),
    url(r'^books/book/(?P<pk>\d+)/$', books_view.book_read, name='book-read'),
    url(r'^books/book/(?P<pk>\d+)/update/$', books_view.BookUpdate.as_view(), name='book-edit'),
    url(r'^books/book/(?P<pk>\d+)/delete/$', books_view.BookDelete.as_view(), name='book-delete'),

    url(r'^books/valoration/list/', books_view.valoration, name='valoration-list'),
    url(r'^books/valoration/create/$', books_view.ValorationCreate.as_view(), name='valoration-add'),
    url(r'^books/valoration/(?P<pk>\d+)/update/$', books_view.ValorationUpdate.as_view(), name='valoration-edit'),
    url(r'^books/valoration/(?P<pk>\d+)/delete/$', books_view.ValorationDelete.as_view(), name='valoration-delete'),

    url(r'^books/querys/last/', books_view.valoration, name='query-books-last'),
    url(r'^books/querys/valued/', books_view.valoration, name='query-books-valued'),

]

