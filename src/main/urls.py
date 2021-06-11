from django.urls import path
from .views import (
    movieListView,
    movieDetailView,
    writeCommentView,
    savedMovieListView,
    ajaxFilterMovieListView,
    searchMovieListView,
    loadMore,
    updateSaved
)

app_name = "main"

urlpatterns = [
    path("", movieListView.as_view(), name="movie-list"),
    path("ajax-filter/", ajaxFilterMovieListView.as_view(), name="ajax-filter"),
    path("load-more/", loadMore, name="load-more"),
    path("update-saved/", updateSaved, name="update-saved"),
    path("search/", searchMovieListView.as_view(), name="search"),
    path("saved/", savedMovieListView.as_view(), name="saved-movie-list"),
    path("<slug:slug>/", movieDetailView.as_view(), name="movie-detail"),
    path("comment/<int:pk>/", writeCommentView, name="write-comment"),
]
