from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

class MySite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('My personal Django')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('My personal Django')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('My personal Django administration')

mysite = MySite()
