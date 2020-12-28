from django.shortcuts import render


def index(request):
    """View for index page."""
    context = {}
    return render(request, 'index.html', context)


def movie(request):
    """View for movie page."""
    context = {}
    return render(request, 'movie.html', context)

