from django .db import models 
from core_profile .models import Profile 

class GalleryMedia (models .Model ):

    ON_CHECKING ='on_checking'
    REJECTED ='rejected'
    APPROVED ='approved'

    STATUS_CHOICES =[
    (ON_CHECKING ,'On_checking'),
    (REJECTED ,'Rejected'),
    (APPROVED ,'Approved'),
    ]

    profile_id =models .ForeignKey (Profile ,on_delete =models .CASCADE ,related_name ='student_id')
    media =models .FileField (upload_to ='gallery_images/')
    status =models .CharField (max_length =15 ,choices =STATUS_CHOICES ,default =ON_CHECKING )
    upload_date =models .DateTimeField (auto_now_add =True )
    uploaded_by =models .ForeignKey (Profile ,on_delete =models .CASCADE ,related_name ='uploader')
