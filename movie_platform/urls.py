from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    re_path(r'^movie/genre/(?P<genre>[-\w]+)$', views.genre, name='genre'),
    re_path(r'^detail/(?P<slug>[-\w]+)$', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.history, name='dashboard'),
    re_path(r'^add_to_cart/(?P<slug>[-\w]+)$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove_from_cart/(?P<slug>[-\w]+)$', views.remove_from_cart, name='remove_from_cart'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
]
