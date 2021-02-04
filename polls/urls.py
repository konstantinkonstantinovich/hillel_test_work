from django.urls import path

from . import views



app_name = 'polls'

urlpatterns = [
    path('success/', views.success, name='success'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('registrate/', views.LoginForm.as_view(), name='registrate'),
]
