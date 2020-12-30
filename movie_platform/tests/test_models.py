from django.test import TestCase
from django.urls import reverse, resolve

from movie_platform.models import Genre

from movie_platform.views import genre


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Genre.objects.create(Name='Romance')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('Name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('Name').max_length
        self.assertEqual(max_length, 50)

    def test_movie_genre_view_success_status_code(self):
        url = reverse('genre', kwargs={'genre': 'Romance'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
