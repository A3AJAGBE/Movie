from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    re_path(r'^movie/(?P<pk>\d+)$', views.detail, name='detail'),
    re_path(r'^movie/(?P<genre>[-\w]+)$', views.genre, name='genre'),
    path('cart/', views.cart, name='cart'),
    path('accounts/', include('allauth.urls')),
]
