from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

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


@login_required
def cart(request):
    """View for cart page."""
    context = {}
    return render(request, 'cart.html', context)


@login_required()
def add_to_cart(request, slug):
    m = get_object_or_404(Movie, slug=slug)
    order_item = OrderItem.objects.create(
        Movie=m,
        Customer=request.user,
        Complete=False
    )
    order_check = Order.objects.filter(Customer=request.user, Complete=False)
    if order_check.exists():
        order = order_check[0]
        # check if the order item is in the order
        if order.Movie.filter(Movie__slug=m.slug).exists():
            messages.warning(request, f'"{m}" is in the shopping bag.')
            return redirect('detail', slug=slug)
        else:
            order.Movie.add(order_item)
            messages.success(request, f'"{m}" added to the shopping bag.')
            return redirect('detail', slug=slug)
    else:
        Date = timezone.now()
        order = Order.objects.create(Customer=request.user, Date_Ordered=Date)
        order.Movie.add(order_item)
        messages.success(request, f'"{m}" added to the shopping bag.')
        return redirect('detail', slug=slug)


@login_required()
def remove_from_cart(request, slug):
    m = get_object_or_404(Movie, slug=slug)
    order_check = Order.objects.filter(
        Customer=request.user,
        Complete=False
    )
    if order_check.exists():
        order = order_check[0]
        if order.Movie.filter(Movie__slug=m.slug).exists():
            order_item = OrderItem.objects.filter(
                Movie=m,
                Customer=request.user,
                Complete=False
            )[0]
            order.Movie.remove(order_item)
            order_item.delete()
            messages.success(request, f'"{m}" removed from the shopping bag')
            return redirect('detail', slug=slug)
        else:
            messages.warning(request, 'This movie not in the shopping bag')
            return redirect('detail', slug=slug)
    else:
        messages.warning(request, 'The shopping bag is empty')
        return redirect('detail', slug=slug)

