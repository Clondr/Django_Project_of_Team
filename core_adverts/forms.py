from django import forms
from core_adverts.models import *


class CreateAdvertForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['advert_title', 'content', 'content_image']
        widgets = {
            'advert_title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }