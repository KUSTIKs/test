from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile


# Create your models here.

class SavedMovie(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    movie = models.ManyToManyField("main.Movie", related_name="savedmovie_movie", verbose_name="movie")
    created_date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.profile.user.get_username()

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name_plural = "Categories"

class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=150, unique=True)
    icon_name = models.CharField(max_length=50, default="film-frames")

    def __str__(self):
        return self.name

class Star(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="stars/image/", default="media/stars/photo/7.png")

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    year = models.PositiveSmallIntegerField()
    poster = models.ImageField(upload_to="movies/poster", null=True, height_field=None, width_field=None, max_length=None)
    country = models.CharField(max_length=100)
    genres = models.ManyToManyField("main.Genre", verbose_name="genres")
    short = models.ImageField(blank="true", upload_to="movies/shortcut", null=True, height_field=None, width_field=None, max_length=None)
    slug = models.SlugField(max_length=150, unique=True) 
    video_id = models.SlugField(max_length=200, default="ykw5NFywYuw")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    actors = models.ManyToManyField(Star, related_name="movie_actor")
    directors = models.ManyToManyField(Star, related_name="movie_director")
    hide = models.BooleanField(default=False)
    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('main:movie-detail', kwargs={"slug": self.slug})

    def get_trailer_url(self):
        return f"https://youtube.com/embed/{self.video_id}"


    def __str__(self):
        return self.title

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.profile.user.get_username}=>{self.movie.title}"

    class Meta:
        ordering = ("-created_date", "-profile__user__username")




    