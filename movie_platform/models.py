from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """This model is for the movie genre."""
    Name = models.CharField(max_length=50, null=False, unique=True,
                            help_text='Enter a movie genre (e.g. Sci-Fi)')

    def __str__(self):
        """String for representing the Model object."""
        return self.Name


VIEW_RATING = (
    ('G', 'General Audiences'),
    ('PG', 'Parental Guidance Suggested'),
    ('PG-13', 'Parents Strongly Cautioned'),
    ('R', 'Restricted'),
    ('NC-17', 'Adults Only')
)


class Movie(models.Model):
    """This model is for the movies."""
    Title = models.CharField(max_length=150, null=False, unique=True)
    Summary = models.TextField(max_length=800, null=False, help_text='Enter a summary of the movie')
    Image = models.FileField(upload_to='posters/', null=False)
    Genre = models.ManyToManyField(Genre, related_name='movie', help_text='Select a genre for this movie')
    Link = models.CharField(max_length=300, null=False)
    Price = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    Discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    Rating = models.CharField(choices=VIEW_RATING, max_length=5, default='G')
    Uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model objects."""
        return self.Title

    def get_genre(self):
        """Return the genres"""
        return ",".join([str(g) for g in self.Genre.all()])

    get_genre.short_description = 'Genre'


class Order(models.Model):
    """This model is for user order."""
    Customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Date_Ordered = models.DateTimeField(auto_now_add=True)
    Complete = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model objects."""
        return str(self.id)


class OrderItem(models.Model):
    """This model is for order item."""
    Movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, blank=True, null=True)
    Order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    Quantity = models.IntegerField(default=1)
    Date_Added = models.DateTimeField(auto_now_add=True)
