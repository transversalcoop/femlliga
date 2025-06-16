import io
import base64
import matplotlib
import pandas as pd

from textwrap import fill as wrap

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _

matplotlib.use("AGG")

import matplotlib.pyplot as plt


def limit_str(x):
    x = str(x)
    if len(x) < 80:
        return x
    return x[:80].strip() + "..."


class Content(models.Model):
    description = models.CharField(max_length=1000)
    content = models.JSONField()

    def __str__(self):
        return self.description


class Topic(models.Model):
    index = models.IntegerField(default=1, unique=True)
    name = models.CharField(max_length=1000, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["index"]

    def __str__(self):
        return f"{self.index}. {self.name}"

    def next_topic(self):
        try:
            return Topic.objects.get(index=self.index + 1)
        except:
            return


class Question(models.Model):
    index = models.IntegerField(default=1)
    question = models.CharField(max_length=1000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        ordering = ["index"]
        unique_together = ["index", "topic"]

    def __str__(self):
        return f"{self.topic.index}.{self.index} {self.question}"

    def previous_questions(self, request):
        lst = []
        for question in self.topic.questions.filter(index__lt=self.index):
            lst.append(question)

        return lst

    def next_question_or_topic(self):
        try:
            return Question.objects.get(topic=self.topic, index=self.index + 1), True
        except Exception:
            return self.topic.next_topic(), False

    def plot(self):
        data = [[a.count] for a in self.answers.all().order_by("-code")]
        index = [
            wrap(limit_str(a), width=20) for a in self.answers.all().order_by("-code")
        ]
        df = pd.DataFrame(data, columns=["Respostes"], index=index)
        df.plot.barh(title=wrap(self.question, width=50), rot=0, figsize=(6, 6))
        b = io.BytesIO()
        plt.tight_layout()
        plt.savefig(b, format="png")
        plt.close()
        b.seek(0)
        return base64.b64encode(b.read()).decode("utf-8")


class Answer(models.Model):
    CODE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    code = models.CharField(max_length=1, choices=CODE_CHOICES)
    answer = models.CharField(max_length=1000)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ["code"]
        unique_together = ["code", "question"]

    def __str__(self):
        return f"{self.code}. {self.answer}"


class Page(models.Model):
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=1000)
    content = CKEditor5Field()

    def __str__(self):
        return self.title


class Feedback(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="feedback"
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.question} | {self.content}"
