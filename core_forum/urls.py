from django .urls import path 
from core_forum .views import *


urlpatterns =[
path ('forum/',forum ,name ='forum'),
path ('forum/create/',create_forum_post ,name ='create-forum-post'),
path ('forum/edit/<int:pk>/',edit_forum_post ,name ='edit-forum-post'),
path ('forum/delete/<int:pk>/',delete_forum_post ,name ='delete-forum-post'),
path ('create-forum-comment/<int:post_id>/',create_forum_comment ,name ='create-forum-comment'),
path ('delete-forum-comment/<int:forum_comment_id>/<int:post_id>/',delete_forum_comment ,name ='delete-forum-comment'),
path ('edit-forum-comment/<int:forum_comment_id>/<int:post_id>/',edit_forum_comment ,name ='edit-forum-comment'),
path ('forum-comments-list/<int:post_id>/',forum_comments_list ,name ='forum-comments-list'),
path ('forum-comment-detail/<int:forum_comment_id>/<int:post_id>/',forum_comment_detail ,name ='forum-comment-detail'),
]
