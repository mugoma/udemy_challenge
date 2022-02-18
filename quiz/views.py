from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, View
from django.conf import settings
from django.core.exceptions import PermissionDenied
from . import forms, apis

# Create your views here.


class QuizLinkFormView(FormView):
    form_class = forms.QuizURLForm
    template_name = "quiz/forms/url.html"

    def get_success_url(self) -> str:
        return reverse("quiz:quiz_form") + f"?quiz_link={self.quiz_url}"

    def form_valid(self, form):
        self.quiz_url = form.cleaned_data.get("quiz_url")
        return super().form_valid(form)


class QuizFormView(FormView):
    template_name = "quiz/forms/quiz.html"

    def get_form_class(self):
        return forms.generate_generic_form(
            self.quiz_link_resp.get("questions"))

    def dispatch(self, request, *args, **kwargs):
        self.quiz_link = self.request.GET.get("quiz_link")
        self.quiz_link_resp = apis.fetch_quiz_api(self.quiz_link)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args: str, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.template_name="quiz/result.html"
        for name,field in form.fields.items():
            score=0
            field.correct=False
            if str(field.answer)==str(form.cleaned_data[name]):
                field.correct=True
                score+=1

        return self.render_to_response(self.get_context_data(form=form,score=score),
                                       status=302)


class MockQuizResponseView(View):

    def get(self, request, *args, **kwargs):
        data = {
            "title":
            "Mock",
            "questions": [
                {
                    "question_text": "What is 1+1?",
                    "choices": {
                        "1": 1,
                        "2": 2,
                        "3": 3,
                        "4": 4
                    },
                    "answer": "1",
                },
                {
                    "question_text": "Which numbers are even?",
                    "choices": {
                        1: 1,
                        2: 2,
                        3: 3,
                        4: 4
                    },
                    "answer": [2, 4],
                    "multi_answer": True,
                },
            ]
        }
        if settings.DEBUG is True:
            return JsonResponse(data)
        else:
            raise PermissionDenied()