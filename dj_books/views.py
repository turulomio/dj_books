import datetime
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import activate
from django.views.generic import ListView,  DetailView

from books.models import Author

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

def index(request):
    activate("es")
    now = datetime.datetime.now()
    if request.user.is_authenticated:
        t = get_template('times.html')
        html = t.render({'datetime': now, 'user': request.user})
        return HttpResponse(html)
    else:
        return unauthorized(request)
        
def logout_view(request):
    logout(request)
    return redirect('login')
    
    
def change_language(request, lang):
    activate(lang)
    
    
class AuthorList(ListView):
    queryset = Author.objects.order_by('name')
    context_object_name = 'author_list'
    
#class AuthorDetail(DetailView):
#    model = Author
#    def get_context_data(self, **kwargs):
#        context = super(Author, self).get_context_data(**kwargs)
#        context['ci1'] = Author.objects.all()
#        return context
