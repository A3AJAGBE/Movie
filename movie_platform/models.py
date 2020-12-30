from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse


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
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        """String for representing the Model objects."""
        return self.Title

    def get_genre(self):
        """Return the genres"""
        return ", ".join([str(g) for g in self.Genre.all()])

    get_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Title)
        return super().save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug})


class OrderItem(models.Model):
    """This model is for order item."""
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    Complete = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model objects."""
        return self.Movie.Title

    def get_total_movie_price(self):
        return self.Quantity * self.Movie.Price

    def get_movie_discount_price(self):
        return self.Quantity * self.Movie.Discount

    def get_amount_saved(self):
        return self.get_total_movie_price() - self.get_movie_discount_price()

    def get_final_price(self):
        if self.Movie.Discount:
            return self.get_movie_discount_price()
        return self.get_total_movie_price()


STATUS = (
    ('V', 'Valid'),
    ('In', 'Invalid')
)


class Order(models.Model):
    """This model is for user order."""
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    Order_Code = models.CharField(max_length=20, blank=True, null=True)
    Movie = models.ManyToManyField(OrderItem)
    Date_Ordered = models.DateTimeField()
    Complete = models.BooleanField(default=False)
    Payment = models.BooleanField(default=False)
    Coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    Due = models.DateTimeField(null=True, blank=True)
    Status = models.CharField(choices=STATUS, max_length=2, default='V')

    def __str__(self):
        """String for representing the Model objects."""
        return self.Customer.username

    def get_movie(self):
        """Return the genres"""
        return ", ".join([str(m) for m in self.Movie.all()])

    get_movie.short_description = 'Movie'

    def get_total(self):
        total = 0
        for m in self.Movie.all():
            total += m.get_final_price()
        if self.Coupon:
            total -= self.Coupon.Amount
        return total

    @property
    def is_overdue(self):
        order_time = self.Date_Ordered
        due_time = self.Due
        if due_time and order_time > due_time:
            self.Status = 'In'
            self.save()
            return True
        return False


class Payment(models.Model):
    """This model is for payment processing"""
    Stripe_Charge_ID = models.CharField(max_length=50)
    Customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    Amount = models.DecimalField(max_digits=4, decimal_places=2)
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Customer.username


class Coupon(models.Model):
    """This model is for coupon code"""
    Code = models.CharField(max_length=15)
    Amount = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.Code


class Contact(models.Model):
    """This model is for contact."""
    Email = models.EmailField(null=False)
    Subject = models.CharField(max_length=100, null=False, help_text='Enter a heading for your message')
    Message = models.TextField(null=False, help_text='Enter your the content of your message')
    Reply = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model object."""
        return f'Message from {self.Email}'
