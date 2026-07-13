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
]