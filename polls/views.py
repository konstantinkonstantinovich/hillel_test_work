from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

# Create your views here.


def success(request):
    return HttpResponse("SUCCESS!!!")


class RegistrationForm(LoginView):
    model = User
    template_name = "polls/login.html"
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
        return HttpResponseRedirect(self.get_success_url())
