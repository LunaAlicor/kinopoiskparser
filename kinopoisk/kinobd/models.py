from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    mpaa = models.CharField(max_length=50, blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    rating_count = models.CharField(max_length=50, blank=True, null=True)
    imdb_ratings_count = models.CharField(max_length=50, blank=True, null=True)
    imdb_rating = models.CharField(max_length=10, blank=True, null=True)
    positive_ratings = models.CharField(max_length=50, blank=True, null=True)
    negative_ratings = models.CharField(max_length=50, blank=True, null=True)
    country_film = models.CharField(max_length=255, blank=True, null=True)
    film_genre = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    budget = models.CharField(max_length=50, blank=True, null=True)
    worldwide_gross = models.CharField(max_length=50, blank=True, null=True)
    russian_gross = models.CharField(max_length=50, blank=True, null=True)
    premiere_date = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
