

import django .db .models .deletion 
from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ('core_gallery','0001_initial'),
    ('core_profile','0001_initial'),
    ]

    operations =[
    migrations .AddField (
    model_name ='gallerymedia',
    name ='profile_id',
    field =models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='student_id',to ='core_profile.profile'),
    ),
    migrations .AddField (
    model_name ='gallerymedia',
    name ='uploaded_by',
    field =models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='uploader',to ='core_profile.profile'),
    ),
    ]
