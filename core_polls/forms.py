from django import forms
from .models import *

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

PollOptionFormSet = forms.modelformset_factory(
    PollOption,
    fields=['text'],
    widgets={'text': forms.TextInput(attrs={'class': 'form-control'})},
    extra=3,
    can_delete=True,
)