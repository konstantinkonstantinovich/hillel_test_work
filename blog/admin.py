from django.contrib import admin
from django import forms
from .models import Post, Comments

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "publishing_data", "author", "description", "status"]
    fields = ["title", "text", "author", "description", "status"]
    list_filter = ['author', 'status']
    form = PostAdminForm


@admin.register(Comments)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'pub_data', 'post', 'author', 'is_published']
    fields = ['comment', 'post', 'author', 'is_published']
    list_filter = ['author']
