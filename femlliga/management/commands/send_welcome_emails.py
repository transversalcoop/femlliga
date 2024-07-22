import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from femlliga.models import Organization
from femlliga.utils import send_welcome_email


class Command(BaseCommand):
    help = """./manage.py send_welcome_emails
El script enviarà correus a totes les organitzacions registrades recentment"""

    def add_arguments(self, parser):
        parser.add_argument("--send", type=bool)

    def handle(self, *args, **options):
        if not options["send"]:
            print(
                f"{timezone.now()} Dry run, set '--send=true' to actually send emails"
            )

        orgs = Organization.objects.filter(welcome_email_sent=False)
        for org in orgs:
            if timezone.now() < org.date + datetime.timedelta(days=2):
                continue  # wait two days before sending

            if options["send"]:
                print(f"{timezone.now()} Sending email to {org.name}...", end="")
                send_welcome_email(org)
                print(" sent")
            else:
                print(f"{timezone.now()} Skipping {org.name}")
