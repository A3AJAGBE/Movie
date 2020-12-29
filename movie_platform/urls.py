from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    re_path(r'^movie/genre/(?P<genre>[-\w]+)$', views.genre, name='genre'),
    re_path(r'^detail/(?P<slug>[-\w]+)$', views.detail, name='detail'),
    re_path(r'^add_to_cart/(?P<slug>[-\w]+)$', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]