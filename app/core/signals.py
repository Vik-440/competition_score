# core/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import User
from community.models import Community

@receiver(pre_save, sender=User)
def ensure_default_community(sender, instance, **kwargs):
    if not Community.objects.filter(id=1).exists():
        Community.objects.create(
            id=1,
            name='Default Community',
            description='This is the default community',
            expiration_date='2099-12-31',
            status=True
        )