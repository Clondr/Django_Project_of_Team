from django import forms
from .models import *

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SurveyPageForm(forms.ModelForm):
    class Meta:
        model = SurveyPage
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва сторінки (опціонально)'}),
        }

class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ['text', 'question_type']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
        }