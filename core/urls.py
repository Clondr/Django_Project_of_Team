from django .conf import settings 
from django .conf .urls .static import static 
from django .contrib import admin 
from django .urls import path ,include 

urlpatterns =[
path ('admin/',admin .site .urls ),
path ('',include ('core_profile.urls')),
path ('',include ('core_grades.urls')),
path ('',include ('core_polls.urls')),
path ('',include ('core_events.urls')),
path ('',include ('core_portfolio.urls')),
path ('',include ('core_gallery.urls')),
path ('',include ('core_materials.urls')),
path ('',include ('core_forum.urls')),
path ('',include ('core_survey.urls')),
path ('',include ('core_adverts.urls')),
path ('',include ('core_auth_system.urls')),
]

if settings .DEBUG :
    urlpatterns +=static (settings .MEDIA_URL ,document_root =settings .MEDIA_ROOT )
