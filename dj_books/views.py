import datetime
from django.http import HttpResponse, Http404
from django.template.loader import get_template

def hello(request):
    return HttpResponse("Hello world") 
    
    
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
    now = datetime.datetime.now()
    if request.user.is_authenticated:
        t = get_template('times.html')
        html = t.render({'datetime': now})
        return HttpResponse(html)
    else:
        return HttpResponse("You're not logged") 
