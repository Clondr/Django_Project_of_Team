from django .urls import path 
from core_auth_system .views import *


urlpatterns =[
path ('login/',login_view ,name ='login'),
path ('logout/',logout_view ,name ='logout'),
path ('register/',register ,name ='register'),
path ('accept-offer/',accept_offer ,name ='accept_offer'),
path ('',home ,name ='home'),
path ('activate/<uidb64>/<token>/',activate_account ,name ='activate-account'),
]