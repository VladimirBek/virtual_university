from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from django.conf import settings
from users.models import User


@shared_task
def check_last_login():
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if (timezone.now() - user.last_login).days > 30:
                user.is_active = False
                send_mail(
                    subject='Давно вас не было',
                    message='Так как вас давно не было у нас на сайте, ваш аакаунт был закблокирован. '
                            'Для разблокировки напишите нашему администратору.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=user.email,
                    fail_silently=False,
                    auth_user=settings.EMAIL_HOST_USER,
                    auth_password=settings.PASSWORD_YANDEX,
                )
                user.save()
