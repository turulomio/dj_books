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
from django.shortcuts import render, redirect


from books.models import Author,  Book
from .forms import UserForm, ProfileForm

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
    success_url = reverse_lazy('database')
    

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"
    success_url = reverse_lazy('database')

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"
    success_url = reverse_lazy('database')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('database')


