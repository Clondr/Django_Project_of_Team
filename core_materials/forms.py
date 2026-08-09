from django import forms 
from core_materials .models import *


class AddMaterialForm (forms .ModelForm ):
    class Meta :
        model =Materials 
        fields =['title','description','file','url','media_type']
        widgets ={
        'title':forms .TextInput (attrs ={'class':'form-control'}),
        'description':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        'file':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        'url':forms .URLInput (attrs ={'class':'form-control'}),
        'media_type':forms .Select (attrs ={'class':'form-select'}),
        }

        fields =['title',
        'description',
        'file',
        'url',
        'media_type',
        ]

