from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


@shared_task
def send_mail_about_course(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    for subscriber in subscribers:
        send_mail(
            "Обновление материалов курса",
            "Посмотрите обновление",
            EMAIL_HOST_USER,
            [subscriber.user.email],
        )
