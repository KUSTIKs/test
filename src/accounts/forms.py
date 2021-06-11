from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User 
from django.forms import ModelForm
from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__' 
        exclude = ['user']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

