import os
from datetime import date, datetime, timedelta

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, \
    Registration


# Create queries within functions

# 01. Library
def show_all_authors_with_their_books():
    print_log_list = []

    for author in Author.objects.all().order_by('id'):
        author_name = author.name
        author_books = [str(book) for book in author.book_set.all()]
        if not author_books:
            continue
        print_log_list.append(
            f"{author_name} has written - {', '.join(author_books)}!")

    return '\n'.join(print_log_list)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


# Create authors
# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# # Create books associated with the authors
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
#
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )


# print(show_all_authors_with_their_books())
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())

# 02. Music App

def add_song_to_artist(artist_name: str, song_title: str):
    artist_obj = Artist.objects.get(name__exact=artist_name)
    song_obj = Song.objects.get(title__exact=song_title)
    artist_obj.songs.add(song_obj)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist_obj = Artist.objects.get(name__exact=artist_name)
    song_obj = Song.objects.get(title__exact=song_title)
    artist_obj.songs.remove(song_obj)


# # Create artists
# artist1 = Artist.objects.create(name="Daniel Di Angelo")
# artist2 = Artist.objects.create(name="Indila")
#
# Create songs
# song1 = Song.objects.create(title="Lose Fac1e")
# song2 = Song.objects.create(title="Tourner 2Dans Le Vide")
# song3 = Song.objects.create(title="Loyalty3")
# song4 = Song.objects.create(title="Loyalty2")
# song5 = Song.objects.create(title="Loyalty3")
#
# # Add a song to an artist
# add_song_to_artist("Daniel Di Angelo", "Lose Face")
# add_song_to_artist("Indila", "Loyalty2")
# add_song_to_artist("Indila", "Loyalty3")
# add_song_to_artist("Indila", "Loyalty3")
# add_song_to_artist("Indila", "Tourner Dans Le Vide")

# # Get all songs by a specific artist
# songs = get_songs_by_artist("Daniel Di Angelo")
# for song in songs:
#     print(f"Daniel Di Angelo: {song.title}")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Indila")
# for song in songs:
#     print(f"Indila: {song.title}")

# # Remove a song from an artist
# remove_song_from_artist("Daniel Di Angelo", "Lose Face")
#
# # Check if the song is removed
# songs = get_songs_by_artist("Daniel Di Angelo")
#
# for song in songs:
#     print(f"Songs by Daniel Di Angelo after removal: {song.title}")

# 03. Shop

def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.filter(name=product_name).first()
    review_all = product.reviews.all()
    avg_sum = sum([reb.rating
                   for reb in review_all])

    return avg_sum / len(review_all)


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


##Create some products
# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# # Create some reviews for products
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)

# # Run the function to get products without reviews
# products_without_reviews = get_products_with_no_reviews()
# print(f"Products without reviews: {', '.join([p.name for p in products_without_reviews])}")
#
# # # Run the function to delete products without reviews
# delete_products_without_reviews()
# print(f"Products left: {Product.objects.count()}")
#
# # Calculate and print the average rating
# print(calculate_average_rating_for_product_by_name("Laptop"))

# 04. License

def calculate_licenses_expiration_dates():
    print_log_list = []
    licenses_all_ordered = DrivingLicense.objects.all().order_by('-license_number')

    for lc in licenses_all_ordered:
        expiration_date = lc.issue_date + timedelta(days=365)

        print_log_list.append(
            f"License with id: {lc.license_number} expires on {expiration_date}!")

    return '\n'.join(print_log_list)


def get_drivers_with_expired_licenses(due_date):
    minimum_created_date = due_date - timedelta(days=365)
    exp_license = Driver.objects.filter(drivinglicense__issue_date__gt=minimum_created_date)
    return exp_license


# # Create drivers
# driver1 = Driver.objects.create(first_name="Tanya", last_name="Petrova")
# driver2 = Driver.objects.create(first_name="Ivan", last_name="Yordanov")
#
# # Create licenses associated with drivers
# license1 = DrivingLicense.objects.create(license_number="123", issue_date=date(2022, 10, 6), driver=driver1)
# license2 = DrivingLicense.objects.create(license_number="456", issue_date=date(2022, 1, 1), driver=driver2)

# Calculate licenses expiration dates
# expiration_dates = calculate_licenses_expiration_dates()
# print(expiration_dates)

# Get drivers with expired licenses
# drivers_with_expired_licenses = get_drivers_with_expired_licenses(date(2023, 1, 1))
# for driver in drivers_with_expired_licenses:
#     print(f"{driver.first_name} {driver.last_name} has to renew their driving license!")

# 05. Car Registration
def register_car_by_owner(owner: object):
    first_reg_no_car = Registration.objects.filter(car__isnull=True).first()
    first_car_no_own = Car.objects.filter(registration__isnull=True).first()

    first_car_no_own.owner = owner
    first_car_no_own.registration = first_reg_no_car

    first_car_no_own.save()

    first_reg_no_car.registration_date = date.today()
    first_reg_no_car.car = first_car_no_own

    first_reg_no_car.save()
    return (f"Successfully registered {first_car_no_own.model} to {owner.name} with registration"
            f" number {first_reg_no_car.registration_number}.")


# # Create instances of the Owner model
# owner1 = Owner.objects.get(name='Ivelin Milchev')
# owner2 = Owner.objects.create(name='Alice Smith')
#
# # Create instances of the Car model and associate them with owners
# car1 = Car.objects.create(model='Citroen C5', year=2004)
# car2 = Car.objects.create(model='Honda Civic', year=2021)
#
# # Create instances of the Registration model for the cars
# registration1 = Registration.objects.create(registration_number='TX0044XA')
# registration2 = Registration.objects.create(registration_number='XYZ789')

# print(register_car_by_owner(owner1))

# 06. Car Admin Setup
