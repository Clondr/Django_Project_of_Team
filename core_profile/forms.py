from django import forms 


class UploadAvatarForm (forms .Form ):
    avatar =forms .ImageField (
    label ='Завантажити аватар',
    required =False ,
    widget =forms .ClearableFileInput (attrs ={'class':'form-control'})
    )
