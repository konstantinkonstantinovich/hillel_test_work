from django.contrib import admin

from .models import Post, Comments


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "publishing_data"]
    fields = ["title", "text", "publishing_data"]


@admin.register(Comments)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'pub_data']
    fields = ['comment']
