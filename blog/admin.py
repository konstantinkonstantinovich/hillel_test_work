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
    list_display = ["title", "text", "publishing_data", "author", "description"]
    fields = ["title", "text", "author", "description"]
    list_filter = ['author']


@admin.register(Comments)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'pub_data', 'post', 'author']
    fields = ['comment', 'post', 'author']
    list_filter = ['author']
