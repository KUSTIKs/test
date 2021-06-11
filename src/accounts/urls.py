from django.urls import path, include
from .views import (
    loginView,
    logoutView,
    registerView,
    settingsView
)

app_name = "accounts"

urlpatterns = [
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('register/', registerView, name="register"),
    path('settings/', settingsView.as_view(), name="settings"),

]
