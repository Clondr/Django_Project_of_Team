from django import forms 
from django .contrib .auth .models import User 
from django .contrib .auth .forms import UserCreationForm 

class RegisterUserForm (UserCreationForm ):
    first_name =forms .CharField (
    max_length =30 ,
    required =False ,
    widget =forms .TextInput (attrs ={'class':'form-control','placeholder':'Введіть ваше ім\'я (опціонально)'})
    )
    last_name =forms .CharField (
    max_length =30 ,
    required =False ,
    widget =forms .TextInput (attrs ={'class':'form-control','placeholder':'Введіть ваше прізвище (опціонально)'})
    )
    email =forms .EmailField (
    required =False ,
    help_text ='Опціональне поле. Якщо вказати, буде надіслано листа для активації.',
    widget =forms .EmailInput (attrs ={'class':'form-control','placeholder':'Введіть вашу електронну пошту (опціонально)'})
    )

    class Meta :
        model =User 
        fields =('username','password1','password2','email','first_name','last_name')