import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")

app = Celery("materials")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings

def get_subscribed_users(course):
    from users.models import User
    return User.objects.filter(subscription__course=course)

@shared_task
def send_course_update_email(course_id):
    from materials.models import Course
    course = Course.objects.get(id=course_id)
    subscribers = get_subscribed_users(course)
    
    if subscribers:
        subject = f"Update: {course.name}"
        message = f"The course '{course.name}' has been updated. Check the new content!"
        recipient_list = [user.email for user in subscribers]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    return f"Sent updates to {len(subscribers)} users."

@shared_task
def deactivate_inactive_users():
    from users.models import User
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__gt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
    return f"Deactivated {inactive_users.count()} inactive users."

@shared_task
def check_and_send_lesson_update(course_id, last_course_update_time):
    time_threshold = now() - timedelta(hours=4)
    if last_course_update_time < time_threshold:
        send_course_update_email.delay(course_id)
