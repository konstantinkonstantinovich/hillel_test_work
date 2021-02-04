from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('success/', views.success, name='success'),
    path('registration/', views.RegistrationForm.as_view(), name='registration'),
]