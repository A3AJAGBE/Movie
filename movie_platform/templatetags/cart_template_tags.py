from django import template
from movie_platform.models import Order, Contact

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(Customer=user, Complete=False)
        if qs.exists():
            return qs[0].Movie.count()
    return 0


@register.filter
def contact_count(user):
    if user.is_staff:
        qs = Contact.objects.filter(Reply=False)
        if qs.exists():
            return qs.count()
    return 0
