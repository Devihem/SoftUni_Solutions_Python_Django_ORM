from django.db import models
from django.core.validators import *
from django.db.models import Count


# Create your models here.


# Pretend like is in the custom_manager.py
class DirectorManager(models.Manager):
    class Meta:
        proxy = True

    def get_directors_by_movies_count(self):
        return self.annotate(movies_count=Count('directors')).order_by('-movies_count', 'full_name')


class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), ]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )


class Movie(models.Model):
    GENRE_CHOICE = (('Action', 'Action'),
                    ('Comedy', 'Comedy'),
                    ('Drama', 'Drama'),
                    ('Other', 'Other'))

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        blank=True,
        null=True,
    )

    genre = models.CharField(
        max_length=100,
        choices=GENRE_CHOICE,
        validators=[MaxLengthValidator(6)],
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False
    )

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='directors'
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        null=True,
        on_delete=models.SET_NULL,
        related_name='starring_actors'
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='actors'
    )
