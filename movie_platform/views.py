from django.shortcuts import render


def index(request):
    """View for index page."""
    context = {}
    return render(request, 'index.html', context)
