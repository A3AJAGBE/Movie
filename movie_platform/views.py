from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
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


def genre(request, genre):
    """View function to filter movies according to the genre."""
    movies = Movie.objects.filter(
        Genre__Name__contains=genre
    ).order_by('-Uploaded_on')
    num_movies = movies.count()
    context = {
        "genre": genre,
        "movies": movies,
        "num_movies": num_movies
    }
    return render(request, 'genre.html', context)


def detail(request, slug):
    """View function to display the movie detail page."""
    movie_detail = get_object_or_404(Movie, slug=slug)
    context = {
        "movie": movie_detail,
    }
    return render(request, 'detail.html', context)


def cart(request):
    """View for cart page."""
    customer = request.user
    order, created = Order.objects.get_or_create(Customer=customer, Complete=False)
    items = order.orderitem_set.all()
    context = {
        "item": items,
    }
    return render(request, 'cart.html', context)

