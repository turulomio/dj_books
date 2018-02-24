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
from dj_books.admin import mysite

from django.contrib.auth import views as auth_views
from dj_books.views import  current_datetime,  hours_ahead,  home, AuthorList, database,  profile_edit,  change_password
urlpatterns = [
    url(r'^admin/', mysite.urls),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d+)/$', hours_ahead),
    url(r'^$', auth_views.login, {'template_name': 'admin/login.html'}), 
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}), 
    url(r'^home/$', home, name='home'),
    url(r'^authors/$', AuthorList.as_view()),
    url(r'^database/$', database), 
    url(r'^profile/$', profile_edit), 
    url(r'^password/$', change_password),
]
