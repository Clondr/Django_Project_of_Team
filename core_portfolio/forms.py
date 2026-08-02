from django import forms
from core_portfolio.models import *
from django.forms import inlineformset_factory


class PortfolioAddForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ['title',
                  'description', 
                  ]

class PortfolioMediaForm(forms.ModelForm):

    class Meta:
        model = PortfolioMedia
        fields = [
            'image',
            'file',
            'url',
            'media_type',
        ]

PortfolioMediaFormSet = inlineformset_factory(
    Portfolio,
    PortfolioMedia,
    form=PortfolioMediaForm,
    extra=8,
    can_delete=True
)