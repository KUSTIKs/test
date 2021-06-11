from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib import messages
from django.utils.translation import ngettext

from .models import (
    Category,
    Comment,
    Genre,
    Movie,
    SavedMovie,
    Star
)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("name", )

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    # readonly_fields = ("user",)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "slug", "video_id", "hide")
    list_display_links = ("title", )
    list_filter = ("year", "genres", "category")
    search_fields = ("title", "year", "genres__name")
    inlines = [CommentInline,]
    readonly_fields = ("get_poster_image", "get_short_image", "get_trailer_video")
    save_on_top = True
    save_as = True
    list_editable = ("hide",)
    actions = ["hide", "show"]
    fieldsets = (
        ( None, {
            "fields": (("title", "slug", "hide"),)
        }),
        ( "Movie info", {
            "fields": (("video_id" , "get_trailer_video"), ("country", "year", "duration"), ("description",), ("genres", "category"),)
        }),
        ( "Stars", {
            "fields": (("actors","directors"),)
        }),
        ( "Media", {
            "fields": ("poster","get_poster_image", "short", "get_short_image",)
        }),
    )
    
    def get_poster_image(self, obj, width=100, height=150):
        return mark_safe(f"<div class='image-wrapper' style='height:{height}px; width:{width}px; position:relative'><img style='height:100%; width: 100%; top:0; left:0; position: absolute; object-fit: cover' src= {obj.poster.url} /><div />")
    get_poster_image.short_description = "poster"

    def get_short_image(self, obj, width=160, height=90):
        return mark_safe(f"<div class='image-wrapper' style='height:{height}px; width:{width}px; position:relative'><img style='height:100%; width: 100%; top:0; left:0; position: absolute; object-fit: cover' src= {obj.short.url} /><div />")
    get_short_image.short_description = "short"

    def get_trailer_video(self, obj):
        try:
            print(color.CYAN, obj.get_trailer_url(), color.END)
            return mark_safe(f'<iframe width="100%" src="{ obj.get_trailer_url() }" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
        except Exception as e:
            print(color.BOLD, color.RED, e, color.END)
    get_trailer_video.short_description = "trailer"

    @admin.action(
        permissions=['change'],
        description="Hide selescted movies",
    )
    def hide(self, request, queryset):
        updated = queryset.update(hide=True)
        self.message_user(request, ngettext(
            '%d movie was successfully hidden.',
            '%d movies were successfully hidden.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(
        permissions=['change'],
        description = "Show selescted movies"
    )
    def show(self, request, queryset):
        updated = queryset.update(hide=False)
        self.message_user(request, ngettext(
            '%d movie was successfully shown.',
            '%d movies were successfully shown.',
            updated,
        ) % updated, messages.SUCCESS)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "profile", "text")
    list_filter = ("movie",)
    search_fields = ("movie__title",)
    readonly_fields = ("profile",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "get_icon")
    list_display_links = ("name", )
    readonly_fields = ("get_icon",)

    def get_icon(self, obj, size= 30):
        return mark_safe(f'<span class="iconify" style="font-size: {size}px;" data-icon="twemoji:{ obj.icon_name }" data-inline="false"></span>')
    get_icon.short_description = "genre icon"

    class Media:
        js = ("https://code.iconify.design/1/1.0.7/iconify.min.js", )
# @admin.register(Save)
# class SaveAdmin(admin.ModelAdmin):
#     list_display = ("id", "user")
#     list_display_links = ("user", )

@admin.register(SavedMovie)
class SavedMovieAdmin(admin.ModelAdmin):
    list_display = ("id",)

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)
    search_fields = ("name",)

    def get_image(self, obj, width=50, height=50):
        return mark_safe(f"<div class='image-wrapper' style='height:{height}px; width:{width}px; position:relative'> <img style='height:100%; width: 100%; top:0; left:0; position: absolute; object-fit: cover' src= {obj.image.url} /><div />")

    get_image.short_description = "photo"


# admin.register(Profile)
admin.site.site_title = "Flicky"
admin.site.site_header = "Flicky"
