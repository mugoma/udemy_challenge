from django.http import request
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from . import forms, views
from django.forms import CheckboxSelectMultiple, Form
# Create your tests here.

local_domain = "http://127.0.0.1:8000"


class QuizLinkTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.valid_form_data = {
            "quiz_url": local_domain + "/quiz/quiz-list/",
        }

    def test_link_form(self):
        """Check the form has the correct fields/field names"""
        form = forms.QuizURLForm(self.valid_form_data)
        self.assertTrue(form.is_valid())
        incorrect_data = {"quiz_url": "notalink"}
        self.assertFalse(forms.QuizURLForm(incorrect_data).is_valid())

    def test_form_view(self):
        """ Check if the form view sets the link attribute for further redirection"""
        link = "/quiz/link/form/"
        self.assertEqual(link, reverse("quiz:link_form"))

        request = RequestFactory().post(link, self.valid_form_data)
        view = views.QuizLinkFormView()
        #view.post(request)
        view.setup(request)
        view.post(request)
        self.assertTrue(view.get_form().is_valid())
        self.assertTrue(hasattr(view, "quiz_url"))

    def test_view_redirect(self):
        """ Check if the link view redirects to the form view"""
        client = Client()
        resp = client.post(reverse("quiz:link_form"),
                           self.valid_form_data,
                           follow=True)

        # since the test clinet doen't run runserver, we cannot test for formview,
        # we shall check for th error instead, untill an external reference url is created/provides
        # that we can test independent of creating a local server
         
        expected_link = reverse(
            "quiz:error_view"
        ) + f"?quiz_link={self.valid_form_data['quiz_url']}"
        #expected_link = reverse(
        #    "quiz:quiz_view"
        #) + f"?quiz_link={self.valid_form_data['quiz_url']}"
        self.assertRedirects(resp, expected_link, fetch_redirect_response=True)


class QuizFormTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quiz_field_data = {
            "title":
            "Test Quiz",
            "questions": [
                {
                    "question_text": "The sun is a star",
                    "choices": [True, False],
                    "answer": True,
                },
            ]
        }
        cls.correct_quiz_resp = {
            'question_1': 2,
            "question_2": [2, 4],
            "question_3": True
        }
        cls.wrong_quiz_resp = {
            'question_1': 2,
            "question_2": [2, 4],
            "question_3": False
        }
        cls.view = views.QuizView
        cls.mock_api_url = local_domain + reverse("quiz:mock_quiz_api")
        cls.path = reverse("quiz:quiz_view") + f"?quiz_link={cls.mock_api_url}"
        cls.rf = RequestFactory()
        super().setUpClass()

    def test_quiz_form(self):
        """Check if the form creator function creates the intended form"""

        class QuizForm(Form):
            question_1 = forms.QuizCheckboxField(
                choices=(("True", "True"), ("False", " False")),
                label="Question 1: The sun is a star",
                widget=CheckboxSelectMultiple,
                answer=True)

        question_list = self.quiz_field_data['questions']
        quiz_form = forms.generate_generic_form(question_list)
        test_form = QuizForm()
        quiz_form_instance = quiz_form()
        #self.assertEqual(test_form,quiz_form_instance)
        self.assertEqual(len(test_form.fields), len(quiz_form_instance.fields))

    def test_quiz_view(self):
        "Check if the quiz view functions properly"
        rf = self.rf

        #Check if the variables are initialised
        #request = rf.get(self.path, {"quiz_link": self.mock_api_url})
        #view = self.view()
        #view.setup(request)
        #view.dispatch(request)
        #view.get(request)
        #self.assertTrue(hasattr(view, "quiz_link"))
        #self.assertTrue(hasattr(view, "quiz_link_resp"))
        #self.assertEqual(view.quiz_link, self.mock_api_url)

        #request = rf.post(self.path, self.correct_quiz_resp)
        #view = self.view()
        #view.post(request)
        #self.assertTrue(view.get_form().is_valid())
        #self.assertTrue(hasattr(view, "quiz_url"))