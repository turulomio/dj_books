
from books.templatetags.mymenu import Menu, Action, Group

from books import __version__, __versiondate__
from django.utils.translation import gettext_lazy as _


def my_context(request):
    # return the version value as a dictionary
    # you may add other values here as well

    menu=Menu(_("My Library"))
    menu.append(Action(_("Search"), None,  "home", False))

    menu.append(Action(_("Add author"), ['books.add_author', ], "author-add", True))

    menu.append(Action(_("My valorations"), ['books.search_valoration'], "valoration-list", True))

    grQuerys=Group(1, _("Queries"), "12", True)
    grQuerys.append(Action(_("Most valued books"), ['books.create_valoration', ], "query_books_valued", True))
    grQuerys.append(Action(_("Unfinished books"), ['books.create_valoration', ], "unfinished-books", True))

    grStatistics=Group(1, _("Statistics"), "13", True)
    grStatistics.append(Action(_("Global"),['books.statistics_global',], "statistics-global", True))
    grStatistics.append(Action(_("User"),['books.statistics_user',], "statistics-user", True))

    menu.append(grQuerys)
    menu.append(grStatistics)



    return {
        'VERSION': __version__, 
        'VERSIONDATE': __versiondate__, 
        'menu': menu,
    }
