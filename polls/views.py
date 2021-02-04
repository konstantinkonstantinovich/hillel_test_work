from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .models import Post

# Create your views here.
from django.views.generic import CreateView


def success(request):
    return HttpResponse("SUCCESS!!!")


class RegistrationForm(CreateView):
    model = User
    template_name = "polls/registration.html"
    fields = ['username', 'email', 'password']
    success_url = '/polls/success/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.cleaned_data['username']
        fake_email = form.cleaned_data['email']
        passw = form.cleaned_data['password']
        User.objects.create_user(
            username=user,
            email=fake_email,
            password=passw
        )
        return redirect(self.success_url)


class LoginForm(LoginView):
    model = User
    template_name = "polls/login.html"
    success_url = '/polls/success/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

