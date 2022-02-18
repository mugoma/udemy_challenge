"""quiz app URL Configuration"""
from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path('link/form/', views.QuizLinkFormView.as_view(), name="link_form"),
    path('form/', views.QuizFormView.as_view(), name="quiz_form"),
    path(
        "quiz-list/",
        views.MockQuizResponseView.as_view(),
    ),
]
