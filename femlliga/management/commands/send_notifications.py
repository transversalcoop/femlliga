from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils import translation, timezone
from django.utils.translation import gettext_lazy as _

from femlliga.models import Organization
from femlliga.utils import (
    get_ordered_needs_and_offers,
    get_periodic_notification_data,
    get_users_to_notify,
    send_periodic_notification,
)


class Command(BaseCommand):
    help = """./manage.py send_notifications
El script enviarà correus a tots els usuaris que tinguen alguna informació per comunicar de les que ha cofigurat que
vol rebre. Només s'enviaran les notificacions si ha passat el temps configurat en el camp `notifications_frequency`"""

    def add_arguments(self, parser):
        parser.add_argument("--send", type=bool)

    def handle(self, *args, **options):
        if not options["send"]:
            print(
                f"{timezone.now()} Dry run, set '--send=true' to actually send emails"
            )

        users = get_users_to_notify()
        site = Site.objects.get(id=settings.SITE_ID)
        sent_count = 0
        for user in users:
            org = Organization.objects.get(creator=user)
            needs, offers = get_ordered_needs_and_offers(org, user.distance_limit_km)
            context = get_periodic_notification_data(site, user, needs, offers)
            if context:
                print(f"{timezone.now()} Sending email to {user.email}...", end="")
                if user.language:
                    translation.activate(user.language)

                if options["send"]:
                    sent = send_periodic_notification(
                        _("Novetats de %(name)s") % {"name": site.name},
                        "email/periodic_notification.html",
                        user,
                        context,
                    )
                else:
                    sent = False

                if sent:
                    sent_count += 1
                    print(f" sent {sent_count}")
                else:
                    print(" not sent")

            else:
                print(f"{timezone.now()} No content for {user.email}")
