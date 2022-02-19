from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import FormView, View, TemplateView
import requests
from . import apis, forms

# Create your views here.


class QuizLinkFormView(FormView):
    form_class = forms.QuizURLForm
    template_name = "quiz/forms/url.html"

    def get_success_url(self) -> str:
        return reverse("quiz:quiz_view") + f"?quiz_link={self.quiz_url}"

    def form_valid(self, form):
        self.quiz_url = form.cleaned_data.get("quiz_url")
        return super().form_valid(form)


class QuizView(FormView):
    template_name = "quiz/forms/quiz.html"

    def get_form_class(self):
        return forms.generate_generic_form(
            self.quiz_link_resp.get("questions"))

    def dispatch(self, request, *args, **kwargs):
        self.quiz_link = self.request.GET.get("quiz_link")
        try:
                    URLValidator()(self.quiz_link)
                    self.quiz_link_resp = apis.fetch_quiz_api(self.quiz_link)
        except Exception:
        #except requests.exceptions.ConnectionError as e:
            return HttpResponseRedirect(
                reverse("quiz:error_view") + "?quiz_link=" + self.quiz_link)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args: str, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.template_name = "quiz/result.html"
        score = 0
        for name, field in form.fields.items():
            field.correct = False
            answer = field.answer
            response = form.cleaned_data[name]

            if type(answer) == list:
                # Convert all elements to strings for comparions.
                # Handles differetn types of objects
                answer = [str(i) for i in answer]
            else:
                answer = str(answer)
                response = str(response)
            if answer == response:
                field.correct = True
                score += 1
        total = len(form.cleaned_data)
        return self.render_to_response(self.get_context_data(form=form,
                                                             score=score,
                                                             total=total),
                                       status=302)


class MockQuizResponseView(View):

    def get(self, request, *args, **kwargs):
        data = {
            "title":
            "Mock",
            "questions": [
                {
                    "question_text": "What is 1+1?",
                    "choices": [1, 2, 3, 4],
                    "answer": 2,
                },
                {
                    "question_text": "Which numbers are even?",
                    "choices": [1, 2, 3, 4],
                    "answer": [2, 4],
                    "multi_answer": True,
                },
                {
                    "question_text": "The sun is a star.",
                    "choices": [True, False],
                    "answer": True,
                },
            ]
        }
        if settings.DEBUG is True:
            return JsonResponse(data)
        else:
            raise PermissionDenied()


class QuizErrorView(TemplateView):
    template_name = "quiz/error.html"

    def get_context_data(self, **kwargs):
        data= super().get_context_data(**kwargs)
        data["quiz_link"]=self.request.GET.get("quiz_link")
        return data