from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.list import ListView

from .models import Post, Comments

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
    template_name = "registration/login.html"
    success_url = '/blog/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/blog/success/')


class RegistrationForm(CreateView):
    model = User
    template_name = "registration/registration.html"
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = '/blog/login/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.cleaned_data['username']
        fake_email = form.cleaned_data['email']
        passw = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create_user(
            username=user,
            email=fake_email,
            password=passw,
            first_name=first_name,
            last_name=last_name,
        )
        return redirect(self.success_url)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'author', 'description', 'image']
    success_url = '/blog/'


class PostDetailView(DetailView):
    model = Post


class PostListView(ListView):
    model = Post
    paginate_by = 1


class CommentsCreteViews(CreateView):
    model = Comments
    fields = ['comment']
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super(CommentsCreteViews, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'blog/userprofile_detail.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = '/blog/'
    fields = ['first_name', 'last_name', 'password', 'email']
    template_name = "blog/userprofile_update.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user
