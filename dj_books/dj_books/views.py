from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render

from books.models import Author,  Book, Valoration
from .forms import UserForm, ProfileForm
from books.tables import TableEasyAuthors,  TableEasyValorations, TableEasyBooks

## @todo Add search to search field to repeat search
## @todo Limit search minimum 3 and maximum 50
def home(request):
    search = request.GET.get('search')
    if search!=None:
        searchtitle=_("Looking for '{}' in Library database".format(search))
        books=Book.objects.filter(Q(title__icontains=search) | Q(year__icontains=search))
        authors=Author.objects.filter(Q(name__icontains=search) | Q(family_name__icontains=search))
        tableeasy_authors=TableEasyAuthors(authors)
        tableeasy_books=TableEasyBooks(books)
        if request.user.has_perm('books.search_valoration'):
            valorations=Valoration.objects.filter(comment__icontains=search)
            tableeasy_valorations=TableEasyValorations(valorations)
    return render(request, 'home.html', locals())

@login_required
def database(request):
    authors= Author.objects.order_by('name')
    books=Book.objects.order_by('title')
    valorations=Valoration.objects.order_by('read_end')
    tableeasy_authors=TableEasyAuthors(authors)
    tableeasy_books=TableEasyBooks(books)
    tableeasy_valorations=TableEasyValorations(valorations)
    return render(request, 'database.html', locals())

@login_required
def valoration(request):
    valorations= Valoration.objects.order_by('read_start')
    tableeasy_valorations=TableEasyValorations(valorations)
    return render(request, 'valoration.html', locals())

@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == 'POST':

        print(request.POST.dict())
        if "button_profile" in request.POST.dict():
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            change_password_form = PasswordChangeForm(request.user)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, _('Your profile was successfully updated!'))

        elif "button_password" in request.POST.dict():
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            change_password_form = PasswordChangeForm(request.user, request.POST)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, _('Your password was successfully updated!'))

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        change_password_form = PasswordChangeForm(request.user)
    change_password_form.fields['old_password'].widget.attrs.pop("autofocus", None)
    return render(request, 'profile.html', locals())



@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.add_author',raise_exception=True), name='dispatch')
class AuthorCreate(CreateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_author',raise_exception=True), name='dispatch')
class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_author',raise_exception=True), name='dispatch')
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.add_book',raise_exception=True), name='dispatch')
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_book',raise_exception=True), name='dispatch')
class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"
    success_url = reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_book',raise_exception=True), name='dispatch')
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('home')


class ValorationCreate(CreateView):
    model = Valoration
    fields = ['book', 'user', 'comment','valoration','read_start','read_end']
    template_name="books/valoration_edit.html"
    success_url = reverse_lazy('valoration-list')

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(ValorationCreate, self).get_form(form_class)
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
        return form

class ValorationUpdate(UpdateView):
    model = Valoration
    fields = ['book', 'user', 'comment','valoration','read_start','read_end']
    template_name="books/valoration_edit.html"
    success_url = reverse_lazy('valoration-list')

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(ValorationUpdate, self).get_form(form_class)
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
        return form

class ValorationDelete(DeleteView):
    model = Valoration
    success_url = reverse_lazy('valoration-list')
