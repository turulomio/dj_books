from books import __version__, __versiondate__

def my_context(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {
        'VERSION': __version__, 
        'VERSIONDATE': __versiondate__, 
    }
