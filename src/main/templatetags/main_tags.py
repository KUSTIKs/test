from django import template
from main.models import Movie, Genre

register = template.Library()


@register.simple_tag()
def get_genre_list(movie_list = Movie.objects.filter(hide=False)):
    # genre_list = set()
    # for movie in movie_list:
    #     for genre in movie.genres.all():
    #         genre_list.add(genre)
    genre_list = Genre.objects.all().distinct()
    return genre_list