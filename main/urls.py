from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
# ---------------------
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('create-advert/', add_advert, name='create-advert'),
    path('delete-advert/<int:pk>/', delete_advert, name='delete-advert'),
    path('update-advert/<int:pk>/', update_advert, name='update-advert'),
    path('adverts-list/', advert_list, name='adverts-list'),
    path('advert-detail/<int:pk>/', advert_detail, name='advert-detail'),
    path('accept-offer/', accept_offer, name='accept_offer'),
    path('', home, name='home'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),
]