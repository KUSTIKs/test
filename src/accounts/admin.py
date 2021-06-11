from django.contrib import admin
from .models import Profile
from django.utils.html import mark_safe
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "get_image")
    list_display_links = ("id", "user")
    readonly_fields = ("get_image",)
    search_fields = ("user__username", "user__email")
    
    def get_image(self, obj, width=50, height=50):
        return mark_safe(f"<div class='image-wrapper' style='height:{height}px; width:{width}px; position:relative'> <img style='height:100%; width: 100%; top:0; left:0; position: absolute; object-fit: cover' src= {obj.image.url} /><div />")
    get_image.short_description = "image"