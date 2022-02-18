import copy
import random

from django import forms


class QuizTextMixin:
    """
    Add the question text as an instance attribute to be accesed by the 
    template during rendering
    """

    def __init__(self, *args, **kwargs):
        if "answer" in kwargs:
            self.answer = kwargs.pop("answer")
        super().__init__(*args, **kwargs)


class QuizURLForm(forms.Form):
    quiz_url = forms.URLField()


class QuizRadioChoiceField(QuizTextMixin, forms.ChoiceField):
    pass


class QuizCheckboxField(QuizTextMixin, forms.MultipleChoiceField):
    pass


def generate_generic_form(question_list):
    if question_list is None:
        raise Exception("Question list improperly configured")
    field_dict = {}
    i = 1
    for question in question_list:
        choices = ((value, key) for key, value in question['choices'].items())
        # if question.get("randomize_choices", False):
        #    random.shuffle(choices)
        if question.get("multi_answer", False):
            field = QuizCheckboxField(choices=choices,
                                      widget=forms.CheckboxSelectMultiple,
                                      label=f"Question {i}: " +
                                      question['question_text'],answer=question['answer'])
        else:
            field = QuizRadioChoiceField(choices=choices,
                                         widget=forms.RadioSelect,
                                         label=f"Question {i}: " +
                                         question['question_text'],answer=question['answer'])
        field_name = "question_" + str(i)
        field_dict[field_name] = field  # GenreicForm,field_name , field
        # GenericForm.
        i += 1

    class QuizMetaClassMixin(forms.forms.DeclarativeFieldsMetaclass):

        def __new__(mcs, name, bases, attrs):
            new_class = super().__new__(mcs, name, bases, attrs)
            class_fields = copy.deepcopy(field_dict)
            new_class.base_fields = class_fields
            new_class.declared_fields = class_fields
            return new_class

    class QuizForm(forms.BaseForm, metaclass=QuizMetaClassMixin):
        pass

    return QuizForm


#data=[{"question_text":"What is 1+1?", "choices":{"1":1, "2":2,"3":3,"4":4}, "answer":"1",}]

# form=generate_generic_form(data)
