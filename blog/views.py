from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView

from .models import Post

# Create your views here.


def index(request):
    num_users = User.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={
            'num_users': num_users,
            'num_visits': num_visits
        },
    )


def success(request):
    return HttpResponse("SUCCESS!!!")


class LoginForm(LoginView):
    model = User
    template_name = "blog/login.html"
    success_url = '/blog/success/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/blog/success/')


class RegistrationForm(CreateView):
    model = User
    template_name = "blog/registration.html"
    fields = ['username', 'email', 'password']
    success_url = '/blog/success/'

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


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'author']
    success_url = '/blog/'


class PostDetailView(DetailView):
    model = Post


class PostListView(ListView):

    model = Post
    paginate_by = 10
