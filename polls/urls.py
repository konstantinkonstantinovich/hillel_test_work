from django.urls import include

from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrate/', views.RegistrationForm.as_view(), name='registrate'),
]
