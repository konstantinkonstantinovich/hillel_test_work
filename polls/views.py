from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.shortcuts import redirect
# Create your views here.


def success(request):
    return HttpResponse("SUCCESS!!!")


class LoginForm(LoginView):
    model = User
    template_name = "polls/login.html"
    success_url = '/polls/success/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/polls/success/')


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
