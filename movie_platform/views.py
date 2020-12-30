from datetime import timedelta

import shortuuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, mail_admins
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import CouponForm, ContactForm, ReviewForm
from .models import *
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    """View for index page."""
    recent = Movie.objects.all().order_by('-Uploaded_on')[:6]
    context = {"recent": recent}
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
    reviews = Review.objects.filter(Movie=movie_detail)

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                Author=request.user,
                Review=form.cleaned_data["Review"],
                Movie=movie_detail,
            )
            review.save()
            messages.success(request, 'Movie review submitted successfully!!!')
    context = {
        "movie": movie_detail,
        "reviews": reviews,
        "form": form,
    }
    return render(request, 'detail.html', context)


def contact(request):
    """View function of contact us page."""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'{form.cleaned_data.get("Subject")} from {form.cleaned_data.get("Email")}'
            message = form.cleaned_data.get('Message')
            try:
                mail = Contact(Email=form.cleaned_data.get("Email"), Subject=form.cleaned_data.get("Subject"), Message=message)
                mail.save()
                mail_admins(subject, message, fail_silently=False)
                messages.success(request, 'Your message was sent successfully, Thanks for contacting us!.')
                return redirect('contact')
            except BadHeaderError:
                messages.warning(request, 'Invalid header found.')
        else:
            messages.warning(request, 'Your message failed to send.')
    return render(request, 'contact.html', {'form': form})


@login_required
def cart(request):
    """View for cart page."""
    try:
        order = Order.objects.get(Customer=request.user, Complete=False)
        context = {
            'order': order,
        }
        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, 'The shopping bag is empty')
        return redirect('movie')


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
            return redirect('cart')
        else:
            order.Movie.add(order_item)
            messages.success(request, f'"{m}" added to the shopping bag.')
            return redirect('cart')
    else:
        Date = timezone.now()
        order = Order.objects.create(Customer=request.user, Date_Ordered=Date)
        order.Movie.add(order_item)
        messages.success(request, f'"{m}" added to the shopping bag.')
        return redirect('cart')


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
            return redirect('cart')
        else:
            messages.warning(request, 'This movie not in the shopping bag')
            return redirect('detail', slug=slug)
    else:
        messages.warning(request, 'The shopping bag is empty')
        return redirect('detail', slug=slug)


@login_required
def payment(request):
    """View for payment page."""
    if request.method == 'POST':
        order = Order.objects.get(Customer=request.user, Complete=False)
        token = request.POST.get('stripeToken')
        amt = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amt,
                currency="eur",
                source=token,
            )

            # Create payment
            pay = Payment()
            pay.Stripe_Charge_ID = charge['id']
            pay.Customer = request.user
            pay.Amount = order.get_total()
            pay.save()

            # Assign payment to order
            order_items = order.Movie.all()
            order_items.update(Complete=True)
            for item in order_items:
                item.save

            order.Complete = True
            order.Payment = True
            order.Order_Code = shortuuid.ShortUUID().random(length=20)
            order.Due = timezone.now() + timedelta(hours=3)
            order.save()

            messages.success(request, "Payment processed successfully")
            return redirect('index')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(request, f"{err.get('message')}")
            return redirect('payment')
        except stripe.error.RateLimitError:
            # Too many requests made to the API too quickly
            messages.warning(request, "To many request error")
            return redirect('payment')
        except stripe.error.InvalidRequestError:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(request, "Invalid Card Information")
            return redirect('payment')
        except stripe.error.AuthenticationError:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(request, "Authentication with stripe failed")
            return redirect('payment')
        except stripe.error.APIConnectionError:
            # Network communication with Stripe failed
            messages.warning(request, "Network Error")
            return redirect('payment')
        except stripe.error.StripeError:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(request, "Something went wrong, Payment processing failed. Kindly, try again")
            return redirect('payment')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(request, "An error occur on our end, we have been notified")
    else:
        order = Order.objects.get(Customer=request.user, Complete=False)
        STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
        context = {'order': order, 'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY, 'CouponForm': CouponForm}
        return render(request, 'payment.html', context)


@login_required
def get_coupon(request, code):
    """View for coupon code verification"""
    try:
        coupon = Coupon.objects.get(Code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, "This coupon does not exist")
        return redirect('payment')


@login_required
def add_coupon(request):
    """View for coupon code"""
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(Customer=request.user, Complete=False)
                order.Coupon = get_coupon(request, code)
                order.save()
                messages.success(request, "Successfully added coupon")
                return redirect('payment')
            except ObjectDoesNotExist:
                messages.warning(request, "Shopping bag is empty")
                return redirect('payment')
        else:
            messages.warning(request, "Invalid Code")
            return redirect('payment')


@login_required
def dashboard(request):
    """View for dashboard"""
    order = Order.objects.filter(Customer=request.user, Complete=True, Payment=True)
    num_rent = order.count()
    context = {
        'order': order,
        'num_rent': num_rent
    }
    return render(request, 'dashboard.html', context)

