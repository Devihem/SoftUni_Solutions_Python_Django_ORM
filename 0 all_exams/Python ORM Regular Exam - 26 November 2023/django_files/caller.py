import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article, Review
from django.db.models import Count, Q, F, Avg


# Import your models here
# Create and run your queries within functions

def get_authors(search_name=None, search_email=None):
    query_run = []
    print_log = []

    if search_name:
        query_run.append(Q(full_name__icontains=search_name))

    if search_email:
        query_run.append(Q(email__icontains=search_email))

    if search_name or search_email:
        authors_selected = Author.objects.filter(*query_run).order_by('-full_name')

        for author in authors_selected:
            print_log.append(
                f"Author: {author.full_name}, email: {author.email}, status: {'Banned' if (author.is_banned) else 'Not Banned'}"
            )

    return '\n'.join(print_log)


def get_top_publisher():
    print_log = ""
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if top_publisher:
        if top_publisher.art_count > 0:
            print_log = f"Top Author: {top_publisher.full_name} with {top_publisher.art_count} published articles."

    return print_log


def get_top_reviewer():
    print_log = ''
    top_rev_auth = Author.objects.annotate(rev_count=Count("review")).order_by('-rev_count', 'email').first()

    if top_rev_auth:
        if top_rev_auth.rev_count > 0:
            print_log = f"Top Reviewer: {top_rev_auth.full_name} with {top_rev_auth.rev_count} published reviews."

    return print_log


def get_latest_article():
    print_log = ''

    last_article = Article.objects.prefetch_related('authors').order_by('published_on').last()

    if last_article:
        article_authors = ', '.join([author.full_name for author in last_article.authors.all().order_by('full_name')])

        article_reviews = last_article.review_set.all()

        avr_review_rating = 0.00
        if article_reviews:
            avr_review_rating = sum([rev.rating for rev in article_reviews]) / len(article_reviews)

        print_log = (f"The latest article is: {last_article.title}."
                     f" Authors: {article_authors}. "
                     f"Reviewed: {len(article_reviews)} times. Average Rating: {avr_review_rating:.2f}.")

    return print_log


def get_top_rated_article():
    print_log = ''
    articles_top_avg_rating = Article.objects.annotate(rev_count=Count('review'),
                                                       avg_score=Avg('review__rating')).filter(
        rev_count__gt=0).order_by('-avg_score', 'title').first()

    if articles_top_avg_rating:
        print_log = f"The top-rated article is: {articles_top_avg_rating.title}, with an average rating of {articles_top_avg_rating.avg_score:.2f}, reviewed {articles_top_avg_rating.rev_count} times."

    return print_log


def ban_author(email=None):
    print_log = "No authors banned."

    if isinstance(email, str):
        author = Author.objects.filter(email__exact=email).first()

        if author:
            num_reviews = 0
            if Review.objects.filter(author=author):
                num_reviews = Review.objects.filter(author=author).count()

            Review.objects.filter(author=author).delete()
            author.is_banned = True
            author.save()

            print_log = f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."

    return print_log
