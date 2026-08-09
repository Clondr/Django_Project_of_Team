from django .urls import path 
from .views import *

urlpatterns =[
path ('change_profile/',change_profile ,name ='change-profile'),
path ('change_detail_profile/<int:pk>/',change_detail_profile ,name ='change-detail-profile'),
path ('profile_detail/<int:pk>/',profile_detail ,name ='profile-detail'),
path ('profile/',profile ,name ='profile'),
]
