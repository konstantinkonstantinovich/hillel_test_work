from .models import Post, Comments
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=Comments)
def create_comments(instance, **kwargs):
    post = 'http://127.0.0.1:8000/blog/post/' + str(instance.post.id)
    author = instance.author.email
    send_mail(
        'New comment',
        'New comment in post:' + post,
        'signal@ex.com',
        ['admin@sd.com', author],
        fail_silently=False,
    )


@receiver(post_save, sender=Post)
def create_post(instance, **kwargs):
    if instance.status == 2:
        post = 'http://127.0.0.1:8000/blog/post/' + str(instance.id)
        send_mail(
            'New post',
            'New post:' + post,
            'signal@ex.com',
            ['admin@sd.com'],
            fail_silently=False,
        )
