from django import template
from movie_platform.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(Customer=user, Complete=False)
        if qs.exists():
            return qs[0].Movie.count()
    return 0
