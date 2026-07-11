from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('change_profile/', change_profile, name='change-profile'),
    path('profile/', profile, name='profile'),
]