

import django .db .models .deletion 
from django .db import migrations ,models 


class Migration (migrations .Migration ):

    initial =True 

    dependencies =[
    ('core_profile','0001_initial'),
    ]

    operations =[
    migrations .CreateModel (
    name ='Portfolio',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('title',models .CharField (max_length =255 )),
    ('description',models .TextField ()),
    ('creation_date',models .DateTimeField (auto_now_add =True )),
    ('creator',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='portfolio_creator',to ='core_profile.profile')),
    ],
    options ={
    'ordering':['-creation_date'],
    },
    ),
    migrations .CreateModel (
    name ='PortfolioMedia',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('image',models .ImageField (blank =True ,null =True ,upload_to ='portfolio_images/')),
    ('file',models .FileField (blank =True ,null =True ,upload_to ='portfolio_files/')),
    ('url',models .URLField (blank =True ,null =True )),
    ('media_type',models .CharField (choices =[('file','Файл'),('image','Картинка'),('url','Посилання')],default ='image',max_length =20 )),
    ('portfolio',models .ForeignKey (on_delete =django .db .models .deletion .CASCADE ,related_name ='portfolio_media',to ='core_portfolio.portfolio')),
    ],
    ),
    ]
