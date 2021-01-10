from django.test import TestCase
from django.urls import reverse

from movie_platform.models import Genre, Coupon


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


class CouponModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Coupon.objects.create(Code='REGULAR', Amount=1.50)

    def test_code_label(self):
        discount = Coupon.objects.get(id=1)
        field_label = discount._meta.get_field('Code').verbose_name
        self.assertEqual(field_label, 'Code')

    def test_code_max_length(self):
        discount = Coupon.objects.get(id=1)
        max_length = discount._meta.get_field('Code').max_length
        self.assertEqual(max_length, 15)

