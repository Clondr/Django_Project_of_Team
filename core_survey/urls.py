from django.urls import path
from .views import *

urlpatterns = [
    path('surveys/', surveys_list, name='surveys-list'),
    path('surveys/create/', create_survey, name='create-survey'),
    path('surveys/<int:pk>/edit/', edit_survey, name='edit-survey'),
    path('surveys/<int:pk>/delete/', delete_survey, name='delete-survey'),
    path('surveys/<int:pk>/take/', survey_take, name='survey-take'),
    path('surveys/<int:pk>/results/', survey_results_user, name='survey-results-user'),
    path('surveys/<int:pk>/results/admin/', survey_results_admin, name='survey-results-admin'),
    path('surveys/<int:pk>/add-page/', add_survey_page, name='add-survey-page'),
    path('surveys/page/<int:pk>/edit/', edit_survey_page, name='edit-survey-page'),
    path('surveys/page/<int:pk>/delete/', delete_survey_page, name='delete-survey-page'),
    path('surveys/question/<int:pk>/delete/', delete_survey_question, name='delete-survey-question'),
]