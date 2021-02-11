from django.conf import settings
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=10000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    publishing_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.TextField(max_length=10000,
                               help_text="Input your comment.")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    pub_data = models.DateTimeField(auto_now_add=True)

