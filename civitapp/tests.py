from django.test import TestCase
from django.urls import reverse

from civitapp.utils import populate_content
from civitapp.models import Topic


class ContentTest(TestCase):
    def test_individual_contents_valid(self):
        populate_content()
        self.assertEqual(Topic.objects.count(), 6)
        count = 0
        for topic in Topic.objects.all():
            for question in topic.questions.all():
                for answer in question.answers.all():
                    count += 1
                    res = self.client.get(reverse("civitapp:answer", args=[answer.id]))
                    self.assertEqual(res.status_code, 200)
                    self.assertContains(res, answer.code + ".")

        self.assertTrue(count > 60)

    def test_joint_contents_valid(self):
        populate_content()
        for topic in Topic.objects.all():
            for question in topic.questions.all():
                for answer in question.answers.all():
                    res = self.client.get(
                        reverse("civitapp:answer_add", args=[answer.id])
                    )
                    self.assertEqual(res.status_code, 200)

                for answer in question.answers.all():
                    self.assertContains(res, answer.code + ".")
