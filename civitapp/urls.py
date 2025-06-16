from django.urls import path

import civitapp.views as views

app_name = "civitapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("topics/", views.TopicListView.as_view(), name="topics"),
    path("report/", views.report, name="report"),
    path("roadmap/", views.roadmap, name="roadmap"),
    path("roadmap/pre/", views.roadmap_pre, name="roadmap_pre"),
    path("roadmap/html/", views.roadmap_html, name="roadmap_html"),
    path("question/<int:pk>/", views.QuestionDetailView.as_view(), name="question"),
    path(
        "question/feedback/", views.CreateFeedbackView.as_view(), name="create_feedback"
    ),
    path(
        "feedback/thanks/", views.FeedbackThanksView.as_view(), name="feedback_thanks"
    ),
    path("answer/<int:pk>/", views.AnswerDetailView.as_view(), name="answer"),
    path(
        "answer/<int:pk>/add/", views.AnswerAddDetailView.as_view(), name="answer_add"
    ),
    path("page/<slug:slug>/", views.PageDetailView.as_view(), name="page"),
]
