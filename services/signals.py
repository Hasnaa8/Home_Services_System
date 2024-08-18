from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=User, dispatch_uid='save_new_user_Customer')
def save_Customer(sender, instance, created, **kwargs):
    if created:
        Customer = Customer(user=instance)
        Customer.save()