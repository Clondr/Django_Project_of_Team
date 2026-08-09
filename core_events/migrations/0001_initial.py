

import django .db .models .deletion 
from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ]

    operations =[
    migrations .CreateModel (
    name ='Calendar',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('name',models .CharField (max_length =255 ,unique =True )),
    ],
    ),
    migrations .CreateModel (
    name ='EventMedia',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('image',models .ImageField (blank =True ,null =True ,upload_to ='events/events_images/')),
    ('file',models .FileField (blank =True ,null =True ,upload_to ='events/events_files/')),
    ('url',models .URLField (blank =True ,null =True )),
    ],
    ),
    migrations .CreateModel (
    name ='Event',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('title',models .CharField (max_length =255 )),
    ('description',models .TextField ()),
    ('date_of_start',models .DateTimeField ()),
    ('date_of_end',models .DateTimeField ()),
    ('calendar',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='events',to ='core_events.calendar')),
    ],
    ),
    ]
