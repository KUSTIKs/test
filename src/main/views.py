from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from .models import (
    Movie,
    Genre,
    SavedMovie,
    Genre,
    Comment,
)
from accounts.models import Profile

from .forms import CommentForm
# Create your views here.

class movieListView(ListView):
    model = Movie
    queryset = Movie.objects.filter(hide=False)
    paginate_by = 18
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["genres"] = Genre.objects.all()
        context["page_name"] = "Main"
        context["profile"] = self.request.user.profile if self.request.user.is_authenticated else None
    
        return context

class savedMovieListView(LoginRequiredMixin, ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'accounts.login'
    paginate_by = 18
    model = Movie
    def get_queryset(self):
        profile = self.request.user.profile
        saved, created = SavedMovie.objects.get_or_create(profile = profile)
        queryset = saved.movie.filter(hide=False)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["profile"] = self.request.user.profile if self.request.user.is_authenticated else None
        context["page_name"] = "Saved"
        return context    

class movieDetailView(DetailView):
    model = Movie
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context["form"] = CommentForm()
        context["profile"] = self.request.user.profile if self.request.user.is_authenticated else None
        context["page_name"] = "Details"
        
        return context

def writeCommentView(request, pk):
    data = json.loads(request.body)
    profile = request.user.profile
    form = CommentForm(data)
    movie = get_object_or_404(Movie, pk=pk)
    comments_list = []
    if form.is_valid():
        form = form.save(commit=False)
        form.movie = movie
        form.profile = profile
        form.save()
        comments_list = list(Comment.objects.filter(pk= form.id).values())
        for item in comments_list:
            profile = get_object_or_404(Profile, id = item['profile_id'])
            item["profile"] = {}
            item["profile"]["username"] = profile.user.username
            item["profile"]["image"] = profile.image.url
            item.pop("profile_id")
    return JsonResponse({"comments": comments_list}, safe=False)

    
class ajaxFilterMovieListView(ListView):
    def get_queryset(self):
        selected_genre_name = self.request.GET.getlist("genre")
        queryset = []
        if (Movie.objects.filter(genres__name__in = selected_genre_name)):
            movie_list = Movie.objects.filter(
                genres__name__in = selected_genre_name,
                hide=False).distinct()
        elif "all" in selected_genre_name:
            movie_list = Movie.objects.filter(hide=False)
        else:
            movie_list = []
        for movie in movie_list:
            movie_distionary = {
                "title": movie.title,
                "poster": movie.poster.url,
                "url": movie.get_absolute_url(),
                "genres": [{"name": genre.name} for genre in movie.genres.all()],
                "is_saved": movie in self.request.user.movie_set.all(),
            }
            queryset.append(movie_distionary)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class searchMovieListView(ListView):
    paginate_by = 18

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
        return context

def loadMore(request):
    data = json.loads(request.body)
    new_length = int(data['commentsShown']) + 3
    request_movie = get_object_or_404(Movie, id = data["movieId"])
    all_comments = int(request_movie.comment_set.all().count())
    comments_list = []
    is_all_shown = True if new_length >= all_comments else False
    if not data['commentsShown'] >= all_comments:
        comments_list = list(request_movie.comment_set.all()[data['commentsShown']:new_length].values())
        for item in comments_list:
            profile = get_object_or_404(Profile, id = item['profile_id'])
            item["profile"] = {}
            item["profile"]["username"] = profile.user.username
            item["profile"]["image"] = profile.image.url
            item.pop("profile_id")
    return JsonResponse({"comments": comments_list, "isAllShown": is_all_shown}, safe=False)

def updateSaved(request):
    data = json.loads(request.body)
    action = data["action"]
    profile = request.user.profile
    request_movie = get_object_or_404(Movie, id = data["movieId"])
    saved, created = SavedMovie.objects.get_or_create(profile = profile)

    if action == 'update':
        if request_movie not in saved.movie.all():
            saved.movie.add(request_movie)
            response_action="added"
        else:
            saved.movie.remove(request_movie)
            response_action="remved"
    else:
        pass
    return JsonResponse({"response_action": response_action}, safe=False)
            

