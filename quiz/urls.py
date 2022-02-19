"""quiz app URL Configuration"""
from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path('link/form/', views.QuizLinkFormView.as_view(), name="link_form"),
    path('form/', views.QuizView.as_view(), name="quiz_view"),
    path(
        "quiz-list/",
        views.MockQuizResponseView.as_view(), name="mock_quiz_api"
    ),
    path("error/",views.QuizErrorView.as_view(),name="error_view"),
    path("",views.QuizLinkFormView.as_view(),name="index")
]
