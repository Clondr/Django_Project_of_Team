from django import forms 
from core_portfolio .models import *
from django .forms import inlineformset_factory 


class PortfolioAddForm (forms .ModelForm ):

    class Meta :
        model =Portfolio 
        fields =['title',
        'description',
        ]
        widgets ={
        'title':forms .TextInput (attrs ={'class':'form-control'}),
        'description':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        }

class PortfolioMediaForm (forms .ModelForm ):

    class Meta :
        model =PortfolioMedia 
        fields =[
        'image',
        'file',
        'url',
        'media_type',
        ]
        widgets ={
        'image':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        'file':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        'url':forms .URLInput (attrs ={'class':'form-control'}),
        'media_type':forms .Select (attrs ={'class':'form-select'}),
        }

PortfolioMediaFormSet =inlineformset_factory (
Portfolio ,
PortfolioMedia ,
form =PortfolioMediaForm ,
extra =8 ,
can_delete =True 
)