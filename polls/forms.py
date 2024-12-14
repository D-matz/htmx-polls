from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
    #    labels = {'question_text': 'Question'}
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
    choice_text = forms.CharField(required=False)
    #    labels = {'choice_text': 'Choice'}
