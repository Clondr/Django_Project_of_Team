

import django .db .models .deletion 
from django .conf import settings 
from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ('core_grades','0001_initial'),
    migrations .swappable_dependency (settings .AUTH_USER_MODEL ),
    ]

    operations =[
    migrations .CreateModel (
    name ='Profile',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('role',models .CharField (choices =[('user','User'),('moderator','Moderator'),('admin','Admin')],default ='user',max_length =10 )),
    ('bio',models .TextField (blank =True ,null =True )),
    ('avatar',models .ImageField (blank =True ,default ='avatars/default.png',null =True ,upload_to ='avatars/')),
    ('user',models .OneToOneField (on_delete =django .db .models .deletion .CASCADE ,to =settings .AUTH_USER_MODEL )),
    ],
    ),
    migrations .CreateModel (
    name ='DigitalDiary',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('content',models .TextField ()),
    ('created_at',models .DateTimeField (auto_now_add =True )),
    ('updated_at',models .DateTimeField (auto_now =True )),
    ('grade',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='digital_diaries',to ='core_grades.grade')),
    ('profile',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='digital_diaries',to ='core_profile.profile')),
    ],
    ),
    ]
