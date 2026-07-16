from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('change_profile/', change_profile, name='change-profile'),
    path('profile/', profile, name='profile'),
    path('profile_detail/<int:profile_id>/', profile_detail, name='profile-detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forum/', forum, name='forum'),
    path('forum/create/', create_forum_post, name='create-forum-post'),
    path('forum/edit/<int:pk>/', edit_forum_post, name='edit-forum-post'),
    path('forum/delete/<int:pk>/', delete_forum_post, name='delete-forum-post'),
    path('register/', register, name='register'),
    path('create-advert/', add_advert, name='create-advert'),
    path('delete-advert/<int:pk>/', delete_advert, name='delete-advert'),
    path('update-advert/<int:pk>/', update_advert, name='update-advert'),
    path('adverts-list/', advert_list, name='adverts-list'),
    path('advert-detail/<int:pk>/', advert_detail, name='advert-detail'),
    path('add_grade/<int:profile_id>/', add_grade, name='add-grade'),
    path('polls/', polls_list, name='polls-list'),
    path('polls/<int:pk>/', poll_detail, name='poll-detail'),
    path('polls/<int:pk>/vote/', poll_vote, name='poll-vote'),
    path('polls/create/', create_poll, name='create-poll'),
    path('polls/<int:pk>/edit/', edit_poll, name='edit-poll'),
    path('polls/<int:pk>/delete/', delete_poll, name='delete-poll'),
    path('create-forum-comment/<int:post_id>/', create_forum_comment, name='create-forum-comment'),
    path('delete-forum-comment/<int:forum_comment_id>/<int:post_id>/', delete_forum_comment, name='delete-forum-comment'),
    path('edit-forum-comment/<int:forum_comment_id>/<int:post_id>/', edit_forum_comment, name='edit-forum-comment'),
    path('forum-comments-list/<int:post_id>/', forum_comments_list, name='forum-comments-list'),
    path('forum-comment-detail/<int:forum_comment_id>/<int:post_id>/', forum_comment_detail, name='forum-comment-detail'),
]