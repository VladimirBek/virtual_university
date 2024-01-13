from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings
from main.models import Course, Subscription


@shared_task
def check_change_course(course_id, date_last, date_updated):
    instance = Course.objects.get(id=course_id)
    emails_list = list(set([us.user.email for us in Subscription.objects.filter(course_id=instance.id)
                            if us.is_active]))
    if date_last != date_updated:
        send_mail(
            subject=f'Уведомление об обновалении курса {instance.name}',
            message=f'Посмотрите, курс {instance.name} обновился',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.PASSWORD_YANDEX,
        )