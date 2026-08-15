from django import forms 
from core_events .models import Event ,EventMedia ,Calendar 
from django .forms import inlineformset_factory 

class AddEventForm (forms .ModelForm ):

    class Meta :
        model =Event 
        fields =['title',
        'description',
        'date_of_start',
        'date_of_end',
        ]
        widgets ={
        'title':forms .TextInput (attrs ={'class':'form-control'}),
        'description':forms .Textarea (attrs ={'class':'form-control','rows':3 }),
        'date_of_start':forms .DateInput (
        attrs ={'type':'date','class':'form-control'},
        format ="%Y-%m-%d",
        ),
        'date_of_end':forms .DateInput (
        attrs ={'type':'date','class':'form-control'},
        format ="%Y-%m-%d",
        ),
        }

    def __init__ (self ,*args ,**kwargs ):
        super ().__init__ (*args ,**kwargs )

        self .fields ['date_of_start'].widget .format ="%Y-%m-%d"
        self .fields ['date_of_end'].widget .format ="%Y-%m-%d"

class EventMediaAddForm (forms .ModelForm ):

    class Meta :
        model =EventMedia 
        fields =['image',
        'file',
        'url',]
        widgets ={
        'image':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        'file':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        'url':forms .URLInput (attrs ={'class':'form-control'}),
        }

EventMediaFormSet =inlineformset_factory (
Event ,
EventMedia ,
form =EventMediaAddForm ,
extra =8 ,
can_delete =True 
)

class CalendarForm (forms .ModelForm ):
    class Meta :
        model =Calendar 
        fields =['name']