from django.utils import timezone

from civitapp.models import Topic, Question, Answer, Content, Page
from civitapp.constants import TOPICS


PAGES = [
    {
        "slug": "legal",
        "title": "Avís legal i política de cookies",
        "file": "civitapp/templates/civitapp/legal.html",
    },
    {
        "slug": "accessibility",
        "title": "Accessibilitat",
        "file": "civitapp/templates/civitapp/accessibility.html",
    },
    {
        "slug": "privacy",
        "title": "Política de proteció de dades",
        "file": "civitapp/templates/civitapp/privacy.html",
    },
]

ANSWER_CODES = list("ABCD")


def populate_content():
    print(f"{timezone.now()} Deleting previous data...")
    Topic.objects.all().delete()
    Question.objects.all().delete()
    Answer.objects.all().delete()
    Content.objects.all().delete()
    Page.objects.all().delete()

    print(f"{timezone.now()} Creating pages...")
    for page in PAGES:
        with open(page["file"], "r") as f:
            Page.objects.create(
                slug=page["slug"],
                title=page["title"],
                content=f.read(),
            )

    print(f"{timezone.now()} Creating topics...")
    for i, t in enumerate(TOPICS):
        t["topic"].index = i + 1
        t["topic"].save()
        for j, q in enumerate(t["questions"]):
            q["question"].index = j + 1
            q["question"].topic = t["topic"]
            q["question"].save()
            for k, a in enumerate(q["answers"]):
                a["answer"].code = ANSWER_CODES[k]
                a["answer"].question = q["question"]
                a["content"].save()
                a["answer"].content = a["content"]

                a["answer"].save()
