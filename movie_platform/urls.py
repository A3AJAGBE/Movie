from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    re_path(r'^movie/(?P<genre>[-\w]+)$', views.genre, name='genre'),
]
