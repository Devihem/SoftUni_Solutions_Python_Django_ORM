import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Movie, Actor
from django.db.models import Count, Q, Avg, F


# Import your models here
# Create and run your queries within functions


def get_directors(search_name=None, search_nationality=None):
    query_run = []

    if search_name:
        query_run.append(Q(full_name__icontains=search_name))

    if search_nationality:
        query_run.append(Q(nationality__icontains=search_nationality))

    print_log = []
    if search_name or search_nationality:

        directors_query = Director.objects.all().filter(*query_run).order_by('full_name')
        print_log = []
        for director in directors_query:
            print_log.append(
                f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    return '\n'.join(print_log)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()
    print_log = []
    if top_director:
        print_log.append(f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}.")

    return ''.join(print_log)


def get_top_actor():
    top_actor = Actor.objects.annotate(m_count=Count('starring_actors')).order_by('-m_count', 'full_name').first()

    if top_actor:
        movies_list = Movie.objects.filter(starring_actor=top_actor)

        if movies_list:
            movie_titles = ', '.join([movie.title for movie in movies_list])
            movie_avg_rating = round(sum([movie.rating for movie in movies_list]) / len(movies_list), 1)

            return f"Top Actor: {top_actor.full_name}, starring in movies: {movie_titles}, movies average rating: {movie_avg_rating}"

    return ""


def get_actors_by_movies_count():
    actors_top_3 = Actor.objects.prefetch_related('actors__actors').annotate(m_count=Count('actors')).order_by(
        '-m_count', 'full_name')[:3]

    print_log = []

    if actors_top_3:
        for actor in actors_top_3:
            if actor.m_count > 0:
                print_log.append(
                    f"{actor.full_name}, participated in {actor.m_count} movies")

    return '\n'.join(print_log)


def get_top_rated_awarded_movie():
    print_log = ''

    top_movie = Movie.objects.filter(
        is_awarded=True).prefetch_related('actors__actors').order_by('-rating', 'title').first()

    if top_movie:
        starring_name = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

        cast = ', '.join([actor.full_name
                          for actor in top_movie.actors.all()])

        print_log = (f"Top rated awarded movie: {top_movie.title},"
                     f" rating: {round(top_movie.rating, 1)}."
                     f" Starring actor: {starring_name}."
                     f" Cast: {cast}.")

    return print_log


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating')+0.1)

    if classic_movies:
        return f"Rating increased for {classic_movies} movies."
    return "No ratings increased."

