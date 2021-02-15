from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _



class Post(models.Model):

    class LoanStatus(models.IntegerChoices):
        BLANKS = 1, _('Blanks')
        IS_PUBLISHED = 2, _('Is_published')
        NO_PUBLISHED = 3, _('No_published')

    status = models.PositiveSmallIntegerField(
        choices=LoanStatus.choices, default=LoanStatus.NO_PUBLISHED, blank=True
    )
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=10000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    publishing_data = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, help_text="Enter a short description")
    image = models.ImageField(upload_to='static/images', blank=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.TextField(max_length=10000,
                               help_text="Input your comment.")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    pub_data = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

