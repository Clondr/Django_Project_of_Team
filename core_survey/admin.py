from django.contrib import admin
from core_survey.models import Survey, SurveyPage, SurveyQuestion, SurveyQuestionOption, SurveyResponse, SurveyAnswer

admin.site.register(Survey)
admin.site.register(SurveyPage)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionOption)
admin.site.register(SurveyResponse)
admin.site.register(SurveyAnswer)
