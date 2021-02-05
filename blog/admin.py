from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "publishing_data"]
    fields = ["title", "text", "publishing_data"]
