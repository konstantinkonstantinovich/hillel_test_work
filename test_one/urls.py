"""test_one URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static

from blog.views import UserProfileUpdateView, UserProfileView, CommentUserProfileView, change_password

urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/user/', UserProfileView.as_view(), name='user-detail'),
    path('accounts/user/<int:pk>/', CommentUserProfileView.as_view(), name='user-comment'),
    path('accounts/user_update/<int:id>', UserProfileUpdateView.as_view(), name='user-update'),
    path('accounts/user/password_update/', change_password, name='change-password'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

