from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

## @todo Change views import to a generic way
from . import views as dj_books_views
from books import views as books_view

urlpatterns = [
    ]
urlpatterns +=i18n_patterns(
    path('admin/', admin.site.urls,  name="admin-site"),
    path('statistics/', books_view.statistics, name='statistics'),
    path('signup/', dj_books_views.signup, name='signup'),
    
    path('account_activation_sent/', dj_books_views.account_activation_sent, name='account_activation_sent'),
    path('activate/(<uidb64>/<token>/',  dj_books_views.activate, name='activate'),
    
    path('login/', LoginView.as_view(template_name='login.html'), name="login"), 
    path('logout/', logout_then_login, name="logout"), 
    path('', books_view.home, name='home'),
    path('database/', books_view.database, name='database'), 
    path('profile/', dj_books_views.profile_edit, name="profile"), 

    path('books/author/create/', books_view.AuthorCreate.as_view(), name='author-add'),
    path('books/author/<int:pk>/', books_view.author_read, name='author-read'), 
    path('books/author/<int:pk>/update/', books_view.AuthorUpdate.as_view(), name='author-edit'),
    path('books/author/<int:pk>/delete/', books_view.AuthorDelete.as_view(), name='author-delete'),

    path('books/book/create/', books_view.BookCreate.as_view(), name='book-add'),
    path('books/book/<int:pk>/', books_view.book_read, name='book-read'),
    path('books/book/<int:pk>/update/', books_view.BookUpdate.as_view(), name='book-edit'),
    path('books/book/<int:pk>/delete/', books_view.BookDelete.as_view(), name='book-delete'),

    path('books/valoration/list/', books_view.valoration, name='valoration-list'),
    path('books/valoration/create/', books_view.ValorationCreate.as_view(), name='valoration-add'),
    path('books/valoration/<int:valoration_id>/update/', books_view.ValorationUpdate.as_view(), name='valoration-edit'),
    path('books/valoration/<int:valoration_id>/delete/', books_view.ValorationDelete.as_view(), name='valoration-delete'),

    path('books/querys/last/', books_view.valoration, name='query-books-last'),
    path('books/querys/valued/', books_view.valoration, name='query-books-valued'),

)

handler403 = 'books.views.error_403'
