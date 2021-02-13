from django.urls import path, include,re_path

from . import views

app_name = 'blog'

urlpatterns = [

    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrate/', views.RegistrationForm.as_view(), name='registrate'),
    path('create/post/', views.PostCreateView.as_view(), name='post-create'),
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comments/', views.CommentsCreteViews.as_view(), name='post-comments'),
    path('user_post/<int:pk>', views.UserPostListView.as_view(), name='user-post')
]
