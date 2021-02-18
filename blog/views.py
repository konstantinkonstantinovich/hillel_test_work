from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import FormView
from django.core.mail import BadHeaderError
from django.views.generic.list import ListView, MultipleObjectMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Post, Comments

from .forms import ContactForm, PostModelForm

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
        messages.add_message(self.request, messages.SUCCESS, 'Authorization success!')
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
        messages.add_message(self.request, messages.SUCCESS, 'Registration success!')
        return redirect(self.success_url)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm
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
        messages.add_message(self.request, messages.SUCCESS, 'Post created!')
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
    paginate_by = 10

    def get_queryset(self):
        return super(PostListView, self).get_queryset().filter(status=2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_users'] = User.objects.count()
        return context


class CommentsCreteViews(CreateView):
    model = Comments
    fields = ['comment']
    success_url = '/blog/'
    template_name = 'blog/comments_form.html'

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
    fields = ['first_name', 'last_name', 'email']
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


class CommentUserProfileView(DetailView):
    model = User
    template_name = 'blog/comment_user_profile.html'


class UserPostListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 5
    template_name = "blog/userpost_list.html"




class BlanksList(ListView):
    model = Post
    template_name = "blog/blanks_list.html"
    paginate_by = 5

    def get_queryset(self):
        return super(BlanksList, self).get_queryset().filter(status=1)


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
        messages.add_message(self.request, messages.SUCCESS, 'Form updated success!')
        return super(BlanksUpdateForm, self).form_valid(form)


class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact_form.html'
    success_url = '/blog/thanks'

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        sender = form.cleaned_data['sender']
        message = form.cleaned_data['message']
        try:
            send_mail(subject, message, sender, ['admin@example.com'])
            messages.add_message(self.request, messages.SUCCESS, 'Message sent')
        except BadHeaderError:
            messages.add_message(self.request, messages.ERROR, 'Message not sent')
        return redirect(self.success_url)


def thanks(request):
    thanks = 'thanks'
    return render(request, 'blog/thanks.html', {'thanks': thanks})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })
