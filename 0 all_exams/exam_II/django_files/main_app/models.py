from django.db import models
from django.core.validators import *
from django.db.models import Count


# Create your models here.

class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return Profile.objects.annotate(orders_count=Count('order')).filter(orders_count__gt=2).order_by(
            '-orders_count')


class Profile(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)])

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        validators=[MaxLengthValidator(15)]
    )

    address = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    objects = ProfileManager()


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)]
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    is_available = models.BooleanField(
        default=True
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )


class Order(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE
    )

    products = models.ManyToManyField(
        to=Product
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    is_completed = models.BooleanField(
        default=False
    )
