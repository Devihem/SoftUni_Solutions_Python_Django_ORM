from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.db.models import Count, Avg, Q, F
from django.core.validators import *


# Create your models here.

# Task1:
class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price, max_price):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms__exact=bedrooms_count)

    def popular_locations(self):
        return self.values('location').annotate(Count('location')).order_by('-location__count', 'id')[:2]


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    objects = RealEstateListingManager()


# Task 2

class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self):
        return round((self.aggregate(Avg('rating'))['rating__avg']), 1)


def rating_validator(value):
    if not 0.0 <= value <= 10.0:
        raise ValidationError("The rating must be between 0.0 and 10.0")


def year_validator(value):
    if not 1990 <= value <= 2023:
        raise ValidationError("The release year must be between 1990 and 2023")


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(validators=[year_validator])
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[rating_validator])
    objects = VideoGameManager()

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix):
        return cls.objects.select_related('billing_info').filter(invoice_number__startswith=prefix)

    @classmethod
    def get_invoices_sorted_by_number(cls):
        return cls.objects.select_related('billing_info').order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str):
        return cls.objects.select_related('billing_info').get(invoice_number=invoice_number)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')

    def get_programmers_with_technologies(self):
        return self.programmers.prefetch_related('projects__technologies_used')


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')

    def get_projects_with_technologies(self):
        return self.projects.prefetch_related('programmers__projects__technologies_used')


class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @classmethod
    def overdue_high_priority_tasks(cls):
        query = Q(priority='High') & Q(is_completed=False) & Q(completion_date__gt=F('creation_date'))
        return cls.objects.filter(query)

    @classmethod
    def completed_mid_priority_tasks(cls):
        query = Q(priority='Medium') & Q(is_completed=True)
        return cls.objects.filter(query)

    @classmethod
    def search_tasks(cls, query: str):
        query = Q(title__contains=query) | Q(description__contains=query)
        return cls.objects.filter(query)

    def recent_completed_tasks(self, days):
        query = Q(is_completed=True) & Q(completion_date__gte=self.creation_date - timedelta(days=days))
        return Task.objects.filter(query)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @staticmethod
    def get_long_and_hard_exercises():
        return Exercise.objects.filter(Q(duration_minutes__gt=30) & Q(difficulty_level__gte=10))

    @staticmethod
    def get_short_and_easy_exercises():
        return Exercise.objects.filter(Q(duration_minutes__lt=15) & Q(difficulty_level__lt=5))

    @staticmethod
    def get_exercises_within_duration( min_duration: int, max_duration: int):
        return Exercise.objects.filter(Q(duration_minutes__lte=max_duration) & Q(duration_minutes__gte=min_duration))

    @staticmethod
    def get_exercises_with_difficulty_and_repetitions( min_difficulty: int, min_repetitions: int):
        return Exercise.objects.filter(Q(difficulty_level__gte=min_difficulty) & Q(repetitions__gte=min_repetitions))

