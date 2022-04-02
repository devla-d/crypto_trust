from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account,Referral


@receiver(post_save, sender=Account)
def create_referral(sender, instance, created, **kwargs):
    if created:
        Referral.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_referral(sender, instance, **kwargs):
    instance.referral.save()