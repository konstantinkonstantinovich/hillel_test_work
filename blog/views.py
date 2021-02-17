from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.core.paginator import Paginator

from .models import Post, Comments

# Create your views here.


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
    fields = ['title', 'text', 'description', 'image', 'status']
    success_url = '/blog/'

    def form_valid(self, form):
        status = form.cleaned_data['status']
        user = self.request.user
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        description = form.cleaned_data['description']
        image = form.cleaned_data['image']
        Post.objects.create(author=user,
                            title=title,
                            text=text,
                            description=description,
                            image=image,
                            status=status,
        )
        return redirect(self.success_url)


class PostDetailView(DetailView, MultipleObjectMixin):
    model = Post
    paginate_by = 2

    def get_context_data(self, **kwargs):

        object_list = Comments.objects.filter(post=self.get_object())
        context = super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class PostListView(ListView):
    model = Post
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_users'] = User.objects.count()
        return context


class CommentsCreteViews(CreateView):
    model = Comments
    fields = ['comment']
    success_url = '/blog/'
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        else:
            if User.objects.filter(username='anon').exists():
                form.instance.author = User.objects.get(username='anon')
            else:
                User.objects.create(username='anon')
                form.instance.author = User.objects.get(username='anon')
        return super(CommentsCreteViews, self).form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = '/blog/'
    fields = ['first_name', 'last_name', 'password', 'email']
    template_name = "blog/userprofile_update.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'blog/userprofile_detail.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserPostListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 5
    template_name = "blog/userpost_list.html"


class BlanksList(ListView):
    model = Post
    template_name = "blog/blanks_list.html"
    paginate_by = 5


class BlanksUpdateForm(DetailView, UpdateView):
    model = Post
    fields = ['title', 'text', 'description', 'image', 'status']
    template_name = 'blog/blanks_update.html'
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if Post.image is None:
            image = form.cleaned_data['image']
            Post.objects.create(image=image)
        return super(BlanksUpdateForm, self).form_valid(form)
