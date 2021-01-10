from django.test import TestCase
from django.urls import resolve, reverse

from movie_platform.views import index, movie, contact


class IndexTest(TestCase):
    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)


class MovieTest(TestCase):
    def test_movie_view_status_code(self):
        url = reverse('movie')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_movie_url_resolves_movie_view(self):
        view = resolve('/movie/')
        self.assertEquals(view.func, movie)


class ContactTest(TestCase):
    def test_contact_view_status_code(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_url_resolves_contact_view(self):
        view = resolve('/contact/')
        self.assertEquals(view.func, contact)
