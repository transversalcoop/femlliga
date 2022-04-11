from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from femlliga.models import *
from femlliga.constants import FROM_EMAIL

class Command(BaseCommand):
    help = """./manage.py send_notifications
El script enviarà correus a tots els usuaris que tinguen peticions pendents de respondre, és a dir, rebudes i sense
especificar si s'inicia la comunicació o no. Només s'enviaran les notificacions si ha passat el temps configurat en el
camp `notifications_frequency`"""

    def handle(self, *args, **options):
        users = self.get_users_to_notify()
        site = Site.objects.get(id=settings.SITE_ID)
        for user in users:
            if self.has_pending_agreements(user):
                print(f"Sending email to {user.email}...", end="")
                self.send_email(user, site)
                print(" sent")

    def get_users_to_notify(self):
        users = CustomUser.objects.exclude(notifications_frequency="NEVER")
        return [u for u in users if self.user_ready_to_notify(u)]

    def user_ready_to_notify(self, user):
        time_from_last_notification = timezone.now() - user.last_notification_date
        return (user.notifications_frequency == "WEEKLY" and time_from_last_notification > timedelta(hours=7*24-1)) or \
            (user.notifications_frequency == "DAILY" and time_from_last_notification > timedelta(hours=23))

    def has_pending_agreements(self, user):
        try:
            o = Organization.objects.get(creator = user)
            a = Agreement.objects.filter(solicitee = o, communication_accepted = None)
            return len(a) > 0
        except:
            return False

    def send_email(self, user, site):
        subject = f"Tens peticions pendents de respondre"
        body = render_to_string("email/notification.html", { "current_site": site })
        msg = EmailMessage(subject=subject, body=body, from_email=FROM_EMAIL, to=[user.email])
        msg.content_subtype = "html"
        msg.send()
        user.last_notification_date = timezone.now()
        user.save()
