from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *


def index(request):
    """View for index page."""
    context = {}
    return render(request, 'index.html', context)


def movie(request):
    """View for movie page."""
    movies = Movie.objects.all().order_by('-Uploaded_on')
    num_movies = Movie.objects.count()
    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "movies": movies,
        "num_movies": num_movies,
        "page_obj": page_obj,
    }
    return render(request, 'movie.html', context)

