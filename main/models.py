from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# Signal to create or save user profile when user is saved
@receiver(post_save, sender='auth.User')
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile when a new user is created
        Profile.objects.create(user=instance)
    else:
        # Save existing profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Profile(models.Model):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username} role: {self.role}'

    def _sync_role_from_user(self):
        if self.user_id:
            if self.user.is_superuser:
                self.role = self.ADMIN
            elif self.user.is_staff:
                self.role = self.MODERATOR
            else:
                self.role = self.USER

    def save(self, *args, **kwargs):
        self._sync_role_from_user()
        super().save(*args, **kwargs)

    def auto_give_role(self):
        self._sync_role_from_user()
        self.save()


class Portfolio(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1555)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)


# Forum
class ForumPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author.username}'


class Grade(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    
    def __str__(self):
        return f'{self.subject} - {self.score} for {self.profile.user.username}'

class DigitalDiary(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='digital_diaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grades = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grades')

    def __str__(self):
        return f'Diary by {self.profile.user.username}'


class Advertisement(models.Model):
    advert_title = models.CharField(max_length=255)
    content = models.TextField()
    content_image = models.ImageField(upload_to='advertisements_images/', blank=True, null=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    announcement_date = models.DateField(auto_now_add=True)

