import datetime
from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


from books.models import Author,  Book
from .forms import UserForm, ProfileForm

def unauthorized(request):
    return HttpResponse("You're not authorized") 
    
    
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now        
    return HttpResponse(html)
    
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be  %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

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
