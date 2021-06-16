from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name="user", on_delete=models.CASCADE)
    image = models.ImageField(default="/", blank=True, upload_to="profiles/image/default-avatar.png")

    def __str__(self):
        return str(self.user.get_username())