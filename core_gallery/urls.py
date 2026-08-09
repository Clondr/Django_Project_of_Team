from django .urls import path 
from core_gallery .views import *


urlpatterns =[
path ('gallery-list/',gallery_media_list ,name ='gallery-list'),
path ('add-to-gallery/<int:profile_id>/',upload_to_gallery ,name ='add-to-gallery'),
path ('approve-addition/<int:media_id>/',approve_addition ,name ='approve-addition'),
path ('moderation-gallery/',moderation_gallery ,name ='moderation-gallery'),
]