from django import forms
from .models import Grade

class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'description']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
