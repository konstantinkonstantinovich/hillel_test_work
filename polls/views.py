from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout

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


class LogoutForm(LogoutView):
    model = User
    template_name = "polls/logout.html"
    success_url = '/polls/success/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""

        logout(self.request)

        return HttpResponseRedirect(self.success_url)

