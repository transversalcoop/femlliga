from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from femlliga.utils import get_users_to_notify, send_notification
from femlliga.models import *

class Command(BaseCommand):
    help = """./manage.py send_notifications
El script enviarà correus a tots els usuaris que tinguen peticions pendents de respondre, és a dir, rebudes i sense
especificar si s'inicia la comunicació o no. Només s'enviaran les notificacions si ha passat el temps configurat en el
camp `notifications_frequency`"""

    def handle(self, *args, **options):
        users = get_users_to_notify()
        site = Site.objects.get(id=settings.SITE_ID)
        sent = 1
        for user in users:
            if self.has_pending_agreements(user):
                print(f"Sending email to {user.email}...", end="")
                send_notification(
                    f"Tens peticions pendents de respondre",
                    "email/notification.html",
                    user,
                    { "current_site": site },
                )
                print("sent {}".format(sent))
                sent += 1

    def has_pending_agreements(self, user):
        try:
            o = Organization.objects.get(creator = user)
            a = Agreement.objects.filter(solicitee = o, communication_accepted = None)
            return len(a) > 0
        except:
            return False
