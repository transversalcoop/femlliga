from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from femlliga.utils import get_users_to_notify, send_notification
from femlliga.models import *

class Command(BaseCommand):
    help = """./manage.py send_reminder
El script enviarà correus a tots els usuaris que tinguen possibilitats de col·laboració. Només s'enviaran les
notificacions si ha passat el temps configurat en el camp `notifications_frequency`"""

    def handle(self, *args, **options):
        users = get_users_to_notify()
        site = Site.objects.get(id=settings.SITE_ID)
        needs, offers = self.get_ordered_needs_and_offers()
        sent = 1
        for user in users:
            need, offer = self.has_matches(user, needs, offers)
            if need["count"] > 0 or offer["count"] > 0:
                print(f"Sending email to {user.email}...", end="")
                send_notification(
                    f"Saps què et pot oferir Fem lliga?",
                    "email/reminder.html",
                    user,
                    {
                        "current_site": site,
                        "need": need,
                        "offer": offer,
                    },
                )
                print("sent {}".format(sent))
                sent += 1

    def has_matches(self, user, needs, offers):
        need, offer = {"name": "", "count": 0}, {"name": "", "count": 0}
        try:
            org = Organization.objects.get(creator=user)
        except:
            return need, offer

        for n in needs:
            if self.has_need(org, n):
                need = {"name": RESOURCE_OPTIONS_READABLE_MAP[(n[0], n[1])], "count": n[2]}

        for o in offers:
            if self.has_offer(org, o):
                offer = {"name": RESOURCE_OPTIONS_READABLE_MAP[(o[0], o[1])], "count": o[2]}

        return need, offer

    def has_need(self, org, n):
        return len(Need.objects.filter(organization=org, resource=n[0], options=n[1])) > 0

    def has_offer(self, org, o):
        return len(Offer.objects.filter(organization=org, resource=o[0], options=o[1])) > 0

    def get_ordered_needs_and_offers(self):
        organizations = Organization.objects.all()
        all_needs, all_offers = [], []
        for resource in RESOURCES_ORDER:
            for option in RESOURCE_OPTIONS_MAP[resource]:
                needs, offers = [], []
                for o in organizations:
                    for x in o.needs.all():
                        if x.has_resource == True and x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                            needs.append(x)
                    for x in o.offers.all():
                        if x.has_resource == True and x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                            offers.append(x)
                all_needs.append((resource, option[0], len(needs)))
                all_offers.append((resource, option[0], len(offers)))

        return sorted(all_needs, key=lambda x: -x[2]), sorted(all_offers, key=lambda x: -x[2])

