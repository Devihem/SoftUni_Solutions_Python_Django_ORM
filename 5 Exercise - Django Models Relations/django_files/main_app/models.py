from django.db import models


# Create your models here.


# 01. Library

class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 02. Music App

class Song(models.Model):
    title = models.CharField(max_length=100)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(to=Song, related_name='artists')


# 03. Shop

class Product(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):
    description = models.CharField(max_length=200)
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(related_name='reviews', blank=True, null=True, to=Product, on_delete=models.CASCADE)


# 04. License

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(to=Driver, on_delete=models.CASCADE)


# 05. Car Registration

class Owner(models.Model):
    name = models.CharField(max_length=50)


class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(related_name='cars', to=Owner, on_delete=models.CASCADE, blank=True, null=True)


class Registration(models.Model):
    registration_number = models.CharField(max_length=10)
    registration_date = models.DateField(blank=True, null=True)
    car = models.OneToOneField(to=Car, on_delete=models.CASCADE, blank=True, null=True)

# 06. Car Admin Setup
