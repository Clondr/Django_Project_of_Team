from django .db import models 
from django .core .exceptions import ValidationError 
from core_profile .models import Profile 

class Calendar (models .Model ):
    name =models .CharField (max_length =255 ,unique =True )

    def __str__ (self ):
        return self .name 

class Event (models .Model ):
    calendar =models .ForeignKey (Calendar ,on_delete =models .CASCADE ,related_name ='events')
    title =models .CharField (max_length =255 )
    description =models .TextField ()
    date_of_start =models .DateTimeField ()
    date_of_end =models .DateTimeField ()
    creator =models .ForeignKey (Profile ,on_delete =models .CASCADE ,related_name ='created_events')

    def __str__ (self ):
        return self .title 

    def clean (self ):
        super ().clean ()

        if self .date_of_start is not None and self .date_of_end is not None :
            if self .date_of_end <self .date_of_start :
                raise ValidationError ("Дата закінчення події не може бути раніше дати її початку!")

class EventMedia (models .Model ):
    event =models .ForeignKey (Event ,on_delete =models .CASCADE ,related_name ='media')
    image =models .ImageField (upload_to ='events/events_images/',blank =True ,null =True )
    file =models .FileField (upload_to ='events/events_files/',blank =True ,null =True )
    url =models .URLField (blank =True ,null =True )

    @property 
    def extention (self ):
        if self .file :
            return self .file .name .split ('.')[-1 ].lower ()
        return None 

    @property 
    def media_type (self ):
        if self .image :
            return 'image'
        if self .file :
            return 'file'
        if self .url :
            return 'url'

    @property 
    def image_url (self ):
        if self .image :
            return self .image .url 
        return None 

    def clean (self ):
        super ().clean ()

        filled =sum ([
        bool (self .image ),
        bool (self .file ),
        bool (self .url ),
        ])

        if filled !=1 :
            raise ValidationError ("Ви можете заповнити тільки одне поле!")

