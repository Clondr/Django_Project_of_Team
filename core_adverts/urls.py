from django.urls import path
from core_adverts.views import *


urlpatterns = [
    path('create-advert/', add_advert, name='create-advert'),
    path('delete-advert/<int:pk>/', delete_advert, name='delete-advert'),
    path('update-advert/<int:pk>/', update_advert, name='update-advert'),
    path('adverts-list/', advert_list, name='adverts-list'),
    path('advert-detail/<int:pk>/', advert_detail, name='advert-detail'),
]