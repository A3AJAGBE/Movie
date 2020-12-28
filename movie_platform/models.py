from django.db import models


class Genre(models.Model):
    """This model is for the movie genre."""
    Name = models.CharField(max_length=50, null=False, unique=True,
                            help_text='Enter a movie genre (e.g. Sci-Fi)')

    def __str__(self):
        """String for representing the Model object."""
        return self.Name
