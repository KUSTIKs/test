from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ProfileForm, UserForm
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def registerView(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            # Profile.objects.create(user=user)
            messages.success(request, f'{user}, your account was creted successfully')
            return redirect('accounts:login')
    context = {
        "form": form,
    }
    return render(request, 'accounts/register.html', context)

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f'you logged in successfully as {username}')
            return redirect("main:movie-list")
        else: 
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
    return render(request, 'accounts/login.html', {})

def logoutView(request):
    logout(request)
    return redirect("main:movie-list")

# class settingsView(generic.UpdateView):
#     form_class = UserChangeForm
#     template_name = 'accounts/settings.html'
#     success_url = reverse_lazy('main:movie-list')

#     def get_object(self):
#         return self.request.user

class settingsView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'accounts.login'
    user_form = UserForm()
    profile_form = ProfileForm()
    template_name = 'accounts/settings.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance= request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'{request.user.username}, your account was updated successfully')
            return redirect("accounts:settings")
        
        context = self.get_context_data(
            user_form = user_form,
            profile_form = profile_form
        )
        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        #     context["user_form"] = user_form
        #     context["profile_form"] = profile_form
        #     return context
        

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
