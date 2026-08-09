from django import forms 
from core_forum .models import *
from django .core .exceptions import ValidationError 


class ForumPostForm (forms .Form ):
    content =forms .CharField (
    max_length =5000 ,
    widget =forms .Textarea (attrs ={'class':'form-control','rows':5 })
    )

    def clean_content (self ):
        content =self .cleaned_data .get ('content','').strip ()
        if len (content )<10 :
            raise ValidationError ('Повідомлення повинно містити мінімум 10 символів.')
        return content 

class AddCommentForumForm (forms .ModelForm ):
    class Meta :
        model =ForumComment 
        fields =['comment_title','comment_content','comment_image']
        widgets ={
        'comment_title':forms .TextInput (attrs ={'class':'form-control'}),
        'comment_content':forms .Textarea (attrs ={'class':'form-control','rows':4 }),
        'comment_image':forms .ClearableFileInput (attrs ={'class':'form-control'}),
        }