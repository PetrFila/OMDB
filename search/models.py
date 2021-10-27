from django.db import models


class Title(models.Model):
    title_types = (
        ('movies', 'Movies'),
        ('series', 'Series')
    )
    # The first item in the (tuple) is the value and second is the label to be shown in the dropdown menu

    title = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=20, choices=title_types, blank=True)
    year = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=500)
    plot = models.CharField(max_length=2000)
    image_link = models.URLField(max_length=2000)
    IMDB_link = models.URLField(max_length=2000)
    # Leaving the field objects without any argument would automatically setup the length to 200 characters