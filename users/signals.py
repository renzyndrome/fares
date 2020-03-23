from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import Profile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_group = Group.objects.get(name='User')
        instance.groups.add(user_group)
        Profile.objects.create(user=instance)

@receiver
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
