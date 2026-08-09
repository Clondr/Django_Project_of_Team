from django .db import models 
from django .db .models .signals import post_save 
from django .dispatch import receiver 
from django .core .exceptions import ValidationError 


@receiver (post_save ,sender ='auth.User')
def save_user_profile (sender ,instance ,created ,**kwargs ):
    if created :
        Profile .objects .create (user =instance )
    else :
        if hasattr (instance ,'profile'):
            instance .profile .save ()


class Profile (models .Model ):
    USER ='user'
    MODERATOR ='moderator'
    ADMIN ='admin'
    ROLE_CHOICES =[
    (USER ,'User'),
    (MODERATOR ,'Moderator'),
    (ADMIN ,'Admin'),
    ]
    role =models .CharField (max_length =10 ,choices =ROLE_CHOICES ,default =USER )
    user =models .OneToOneField ('auth.User',on_delete =models .CASCADE )
    bio =models .TextField (blank =True ,null =True )
    avatar =models .ImageField (upload_to ='avatars/',default ='avatars/default.png',blank =True ,null =True )

    def __str__ (self ):
        return f'Profile of {self .user .username } role: {self .role }'

    def _sync_role_from_user (self ):
        if self .user_id :
            if self .user .is_superuser :
                self .role =self .ADMIN 
            elif self .user .is_staff :
                self .role =self .MODERATOR 
            else :
                self .role =self .USER 

    def save (self ,*args ,**kwargs ):
        self ._sync_role_from_user ()
        super ().save (*args ,**kwargs )

    def auto_give_role (self ):
        self ._sync_role_from_user ()
        self .save ()


class DigitalDiary (models .Model ):
    profile =models .ForeignKey ("core_profile.Profile",on_delete =models .CASCADE ,related_name ='digital_diaries')
    content =models .TextField ()
    created_at =models .DateTimeField (auto_now_add =True )
    updated_at =models .DateTimeField (auto_now =True )
    grade =models .ForeignKey ("core_grades.Grade",on_delete =models .CASCADE ,related_name ='digital_diaries')

    def __str__ (self ):
        try :
            username =self .profile .user .username 
        except Exception :
            username ='unknown'
        return f'Diary by {username }'

    def clean (self ):
        profile_id =getattr (self ,'profile_id',None )
        if not profile_id :
            return 
        profile =Profile .objects .filter (pk =profile_id ).first ()
        if not profile :
            return 
        user =getattr (profile ,'user',None )
        if user and (getattr (user ,'is_staff',False )or getattr (user ,'is_superuser',False )):
            raise ValidationError ('Cannot create DigitalDiary for staff or superuser accounts.')

    def save (self ,*args ,**kwargs ):
        self .full_clean ()
        super ().save (*args ,**kwargs )
