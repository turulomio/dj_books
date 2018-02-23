import datetime
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import activate
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from forms import UserForm, ProfileForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from books.models import Author,  Book

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
def index(request):
    activate("es")
    now = datetime.datetime.now()
    t = get_template('times.html')
    html = t.render({'datetime': now, 'user': request.user})
    return HttpResponse(html)
        
def logout_view(request):
    logout(request)
    return redirect('login')
    
    
def change_language(request, lang):
    activate(lang)
    
@login_required
def database(request):
    activate("es")
    authors= Author.objects.order_by('name')
    books=Book.objects.order_by('title')
    t=get_template("database.html")
    html = t.render({'authors': authors, 'books': books})
    print(request.user, dir(request.user))
    return HttpResponse(html)
    
class AuthorList(ListView):
    queryset = Author.objects.order_by('name')
    context_object_name = 'author_list'
    
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
#class AuthorDetail(DetailView):
#    model = Author
#    def get_context_data(self, **kwargs):
#        context = super(Author, self).get_context_data(**kwargs)
#        context['ci1'] = Author.objects.all()
#        return context
