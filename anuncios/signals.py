from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from anuncios.models import Profile, Post


@receiver(post_save, sender=User)
def on_post_save_user(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(pre_delete, sender=User)
def on_pre_delete_user(sender, instance=None, **kwargs):
    Profile.objects.get(user=instance).delete()
    Post.objects.filter(user=instance).delete()

