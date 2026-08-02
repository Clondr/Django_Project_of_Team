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