

import django .db .models .deletion 
from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ('core_adverts','0001_initial'),
    ('core_profile','0001_initial'),
    ]

    operations =[
    migrations .AddField (
    model_name ='advertisement',
    name ='creator',
    field =models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='creator',to ='core_profile.profile'),
    ),
    ]
