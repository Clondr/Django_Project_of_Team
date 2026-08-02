from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    path('polls/', polls_list, name='polls-list'),
    path('polls/<int:pk>/', poll_detail, name='poll-detail'),
    path('polls/<int:pk>/vote/', poll_vote, name='poll-vote'),
    path('polls/create/', create_poll, name='create-poll'),
    path('polls/<int:pk>/edit/', edit_poll, name='edit-poll'),
    path('polls/<int:pk>/delete/', delete_poll, name='delete-poll'),
]