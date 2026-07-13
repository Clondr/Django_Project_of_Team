from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('change_profile/', change_profile, name='change-profile'),
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forum/', forum, name='forum'),
    path('forum/create/', create_forum_post, name='create-forum-post'),
    path('register/', register, name='register'),
    path('create-advert/', add_advert, name='create-advert'),
    path('delete-advert/<int:pk>/', delete_advert, name='delete-advert'),
    path('update-advert/<int:pk>/', update_advert, name='update-advert'),
    path('adverts-list/', advert_list, name='adverts-list'),
    path('advert-detail/<int:pk>/', advert_detail, name='advert-detail'),
]