from django.db import models

# Create your models here.

# Surveys
class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def pages_count(self):
        return self.pages.count()


class SurveyPage(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='pages')
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Сторінка {self.order} — {self.survey.title}'


class SurveyQuestion(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    TYPE_CHOICES = [(TEXT, 'Текст'), (CHOICE, 'Вибір')]

    page = models.ForeignKey(SurveyPage, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TEXT)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class SurveyQuestionOption(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='survey_responses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('survey', 'user')


class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True)
    choice_answer = models.ForeignKey(SurveyQuestionOption, on_delete=models.SET_NULL, null=True, blank=True)