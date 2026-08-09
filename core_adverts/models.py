from django .db import models 

class Advertisement (models .Model ):
    advert_title =models .CharField (max_length =255 )
    content =models .TextField ()
    content_image =models .ImageField (upload_to ='advertisements_images/',blank =True ,null =True )
    creator =models .ForeignKey ("core_profile.Profile",on_delete =models .CASCADE ,related_name ='creator')
    announcement_date =models .DateField (auto_now_add =True )
