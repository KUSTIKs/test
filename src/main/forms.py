from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ("text", "captcha")
        widgets = {
            "text": forms.TextInput(attrs={"class": "input", "id": "written-comment", "autocomplete": "off", "placeholder": "Write here..."}),
        }