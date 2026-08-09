from django .urls import path 
from core_materials .views import *


urlpatterns =[
path ('materials-list/',materials_list ,name ='materials-list'),
path ('material-detail/<int:material_id>/',material_detail ,name ='material-detail'),
path ('add-material/',add_material ,name ='add-material'),
path ('change-material/<int:material_id>/',change_material ,name ='change-material'),
path ('delete-material/<int:material_id>/',delete_material ,name ='delete-material'),
]