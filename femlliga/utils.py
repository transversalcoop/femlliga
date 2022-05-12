from datetime import datetime, timedelta

from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from femlliga.constants import FROM_EMAIL

def get_users_to_notify():
    users = get_user_model().objects.exclude(notifications_frequency="NEVER")
    return [u for u in users if user_ready_to_notify(u)]

def user_ready_to_notify(user):
    time_from_last_notification = timezone.now() - user.last_notification_date
    return (user.notifications_frequency == "WEEKLY" and time_from_last_notification > timedelta(hours=7*24-1)) or \
        (user.notifications_frequency == "DAILY" and time_from_last_notification > timedelta(hours=23))

def send_notification(subject, template, user, context):
    body = render_to_string(template, context)
    msg = EmailMessage(subject=subject, body=body, from_email=FROM_EMAIL, to=[user.email])
    msg.content_subtype = "html"
    msg.send()
    user.last_notification_date = timezone.now()
    user.save()

def date_intervals(start, end):
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    if (end - start) < timedelta(days=30):
        f = lambda x: x + timedelta(days=1)
    elif (end - start) < timedelta(days=30*3):
        f = lambda x: x + timedelta(days=7)
    else:
        start = start.replace(day=1)
        f = lambda x: add_one_month(x)

    intervals = [start]
    mid = start
    while mid < end:
        mid = f(mid)
        intervals.append(mid)

    return intervals

def add_one_month(t):
    t = t.replace(day=1)
    t = t + timedelta(days=32)
    t = t.replace(day=1)
    return t
