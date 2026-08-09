from django import forms 
from core_gallery .models import *


class GalleryMediaUploadForm (forms .ModelForm ):
    class Meta :
        model =GalleryMedia 
        fields =['media']
        widgets ={
        'media':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        }