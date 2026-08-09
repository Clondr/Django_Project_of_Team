

from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ]

    operations =[
    migrations .CreateModel (
    name ='GalleryMedia',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('media',models .FileField (upload_to ='gallery_images/')),
    ('status',models .CharField (choices =[('on_checking','On_checking'),('rejected','Rejected'),('approved','Approved')],default ='on_checking',max_length =15 )),
    ('upload_date',models .DateTimeField (auto_now_add =True )),
    ],
    ),
    ]
