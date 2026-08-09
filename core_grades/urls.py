from django .urls import path 
from .views import *

urlpatterns =[
path ('add_grade/<int:pk>/',add_grade ,name ='add-grade'),
path ('grades_list/<int:pk>/',list_grades ,name ='list-grades'),
path ('edit_grade/<int:pk>/',edit_grade ,name ='edit-grade'),
path ('delete_grade/<int:pk>/',delete_grade ,name ='delete-grade'),
path ('search_user_for_moderator/',search_user_for_moderator ,name ='search-user-for-moderator'),
]