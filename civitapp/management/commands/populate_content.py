from django.utils import timezone
from django.core.management.base import BaseCommand

from civitapp.utils import populate_content


class Command(BaseCommand):
    help = """./manage.py populate_content [--apply=true]
    Si es marca la opció --apply, esborrarà tot el contingut de la pàgina i el tornarà a crear de zero
    """

    def add_arguments(self, parser):
        parser.add_argument("--apply", type=bool)

    def handle(self, *args, **options):
        if options["apply"]:
            populate_content()
        else:
            print(
                f"{timezone.now()} Dry run, set '--apply=true' to actually populate content"
            )
