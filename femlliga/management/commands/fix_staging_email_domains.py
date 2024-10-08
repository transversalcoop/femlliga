from django.core.management.base import BaseCommand
from django.utils import timezone

from femlliga.models import CustomUser
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = """./manage.py fix_staging_email_domains
El script canviarà els dominis de tots els correus per un domini segur per evitar enviaments de correus erronis en
proves"""

    def add_arguments(self, parser):
        parser.add_argument("--apply", type=bool)

    def handle(self, *args, **options):
        if not options["apply"]:
            print(
                f"{timezone.now()} Dry run, set '--apply=true' to actually fix emails"
            )

        for u in CustomUser.objects.all():
            self.fix_email("user", u, options)

        for e in EmailAddress.objects.all():
            self.fix_email("email", e, options)

    def fix_email(self, typ, x, options):
        count = 0
        original_email = x.email
        while True:
            new_email = self.change_email_domain(original_email, count)
            print(
                f"{timezone.now()} Changing {typ} {original_email} for {new_email}... ",
                end="",
            )
            x.email = new_email
            if options["apply"]:
                try:
                    x.save()
                    print("done")
                    break
                except Exception:
                    print("failed")
                    count += 1
            else:
                print("skipped")
                break

    def change_email_domain(self, email, count):
        index = email.index("@")
        email = email[:index]
        if count > 0:
            email += str(count)
        email += "@example.com"
        return email
