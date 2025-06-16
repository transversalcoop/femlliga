import tempfile
import subprocess

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

from civitapp.models import Topic, Question, Answer, Page, Feedback


def index(request):
    return render(request, "civitapp/index.html", {})


class TopicListView(ListView):
    model = Topic

    def get(self, request, *args, **kwargs):
        if "answers" in request.session:
            del request.session["answers"]
        return super().get(request, *args, **kwargs)


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        return context


class AnswerDetailView(DetailView):
    model = Answer

    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        topic = answer.question.topic
        answers = request.session.get("answers")
        if not answers:
            answers = {}
        answers.setdefault(str(topic.id), {})[str(answer.question.id)] = [answer.id]
        request.session["answers"] = answers
        return render(
            request,
            "civitapp/answer_detail.html",
            {"object": answer, "answers": [answer]},
        )


class AnswerAddDetailView(DetailView):
    model = Answer

    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        topic = answer.question.topic
        answers = request.session.get("answers")
        if not answers:
            answers = {}
        lst = answers.setdefault(str(topic.id), {}).setdefault(
            str(answer.question.id), []
        )
        if answer.id not in lst:
            lst.append(answer.id)
        request.session["answers"] = answers

        return render(
            request,
            "civitapp/answer_detail.html",
            {
                "object": answer,
                "answers": [Answer.objects.get(id=answer_id) for answer_id in lst],
            },
        )


class PageDetailView(DetailView):
    model = Page


class CreateFeedbackView(CreateView):
    model = Feedback
    fields = ["question", "content"]
    success_url = reverse_lazy("civitapp:feedback_thanks")


class FeedbackThanksView(TemplateView):
    template_name = "civitapp/feedback_thanks.html"


def get_session_answers(request):
    a = request.session.get("answers")
    if a:
        return a

    return {}


def roadmap_content(request):
    answers, questions = {}, {}
    session_answers = get_session_answers(request)
    if session_answers:
        for topic_id, question in session_answers.items():
            m = {}
            for question_id, answer_ids in question.items():
                for answer_id in answer_ids:
                    answer = Answer.objects.get(id=int(answer_id))
                    answer.count += 1
                    answer.save()
                    m.setdefault(int(question_id), []).append(answer)
                questions[int(question_id)] = Question.objects.get(id=int(question_id))

            answers[int(topic_id)] = m

    return render_to_string(
        "civitapp/roadmap.html",
        {
            "answers": answers,
            "questions": questions,
            "topics": Topic.objects.all(),
        },
    )


def roadmap(request):
    content = roadmap_content(request)
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        fp.write(content.encode("utf-8"))
        fp.close()

        pdfname = fp.name + ".pdf"
        try:
            cmd = f"cat {fp.name} | wkhtmltopdf --enable-local-file-access -T 1cm -R 1cm -B 1cm -L 1cm - {pdfname}"
            subprocess.check_output(cmd, shell=True)
        except Exception as e:
            print(e.output)

        with open(pdfname, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response["Content-Disposition"] = (
                "attachment; filename=Full de ruta CivitAPP.pdf"
            )
        return response


def roadmap_html(request):
    content = roadmap_content(request)
    return HttpResponse(content)


def roadmap_pre(request):
    return render(
        request,
        "civitapp/roadmap_pre.html",
        {"topics": Topic.objects.all(), "object": None},
    )


@user_passes_test(lambda u: u.is_staff)
def report(request):
    return render(request, "civitapp/report.html", {"topics": Topic.objects.all()})
