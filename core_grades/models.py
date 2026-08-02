from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Grade(models.Model):
    profile = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='grades')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])

    def __str__(self):
        if self.profile_id and self.profile:
            username = self.profile.user.username
        else:
            username = "unknown"
        return f"{self.score} for {username}"   

    def clean(self):
        if not self.profile_id:
            return
        user = getattr(self.profile, "user", None)
        if user and (user.is_staff or user.is_superuser):
            raise ValidationError("Cannot create Grade for staff or superuser accounts.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
