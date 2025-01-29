from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    users_to_block = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in users_to_block:
        user.is_active = False
        user.save()
