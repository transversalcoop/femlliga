import textwrap

from django.core.management.base import BaseCommand

from civitapp.constants import CONTENTS, TOPICS


class Command(BaseCommand):
    help = """./manage.py print_topics"""

    def handle(self, *args, **options):
        for i, t in enumerate(TOPICS):
            print(f"{i+1}. {t['topic'].name}")
            for j, q in enumerate(t["questions"]):
                lst = textwrap.wrap(
                    f"    {i+1}.{j+1}. {q['question'].question}",
                    width=100,
                )
                print("\n         ".join(lst))
