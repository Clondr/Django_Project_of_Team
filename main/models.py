from django.db import models

from core_profile.models import *

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import mimetypes
from urllib.parse import urlparse, parse_qs
# Create your models here.





class DigitalDiary(models.Model):
    profile = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='digital_diaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey("core_grades.Grade", on_delete=models.CASCADE, related_name='digital_diaries')

    def __str__(self):
        try:
            username = self.profile.user.username
        except Exception:
            username = 'unknown'
        return f'Diary by {username}'

    def clean(self):
        # Prevent DigitalDiary being created/assigned to staff or superuser accounts.
        # Use profile_id to avoid accessing related descriptor before assignment.
        profile_id = getattr(self, 'profile_id', None)
        if not profile_id:
            return
        profile = Profile.objects.filter(pk=profile_id).first()
        if not profile:
            return
        user = getattr(profile, 'user', None)
        if user and (getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)):
            raise ValidationError('Cannot create DigitalDiary for staff or superuser accounts.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Advertisement(models.Model):
    advert_title = models.CharField(max_length=255)
    content = models.TextField()
    content_image = models.ImageField(upload_to='advertisements_images/', blank=True, null=True)
    creator = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='creator')
    announcement_date = models.DateField(auto_now_add=True)


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


