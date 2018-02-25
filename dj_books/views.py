import datetime
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect,  get_object_or_404


from books.models import Author,  Book
from .forms import UserForm, ProfileForm,  BookForm, AuthorForm

def unauthorized(request):
    return HttpResponse("You're not authorized") 


@login_required
def home(request):
    now = datetime.datetime.now()
    return render(request, 'home.html', locals())
        
def logout_view(request):
    logout(request)
    return redirect('login')

    
@login_required
def database(request):
    authors= Author.objects.order_by('name')
    books=Book.objects.order_by('title')
    return render(request, 'database.html', locals())
    
class AuthorList(ListView):
    queryset = Author.objects.order_by('name')
    context_object_name = 'author_list'
    
@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', locals())
    
@login_required
@transaction.atomic
def book_edit(request):
    if request.method == 'POST':
        form = BookForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your book was successfully updated!'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = BookForm(request.POST, instance=request.user)
    return render(request, 'books/book_new.html', locals())
    
@login_required
@transaction.atomic
def author_new(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Author was successfully updated!'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = AuthorForm(request.POST)
    return render(request, 'books/author_new.html', locals())
    
    
    
@login_required
@transaction.atomic
def author_edit(request, pk):
    author= get_object_or_404(Author, id=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, _('Author was successfully updated!'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = AuthorForm(request.POST, instance=author)
    return render(request, 'books/author_new.html', locals())

class AuthorCreate(CreateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"
    success_url = reverse_lazy('database')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"
    success_url = reverse_lazy('database')

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/password/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
