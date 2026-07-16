from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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

class Item(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Grade(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='grades')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        try:
            username = self.profile.user.username
        except Exception:
            username = 'unknown'
        return f'{self.score} for {username}'
    
    def clean(self):
        # Prevent Grades being created/assigned to staff or superuser accounts.
        # Use profile_id to avoid accessing the related descriptor when profile
        # hasn't been assigned yet (e.g. form.save(commit=False)).
        profile_id = getattr(self, 'profile_id', None)
        if not profile_id:
            return
        profile = Profile.objects.filter(pk=profile_id).first()
        if not profile:
            return
        user = getattr(profile, 'user', None)
        if user and (getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)):
            raise ValidationError('Cannot assign Grade to staff or superuser accounts.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class DigitalDiary(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='digital_diaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='digital_diaries')

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
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    announcement_date = models.DateField(auto_now_add=True)

class ForumComment(models.Model):
    comment_title = models.CharField(max_length=255)
    comment_content = models.TextField()
    comment_image = models.FileField(upload_to='forum_comments_images/', blank=True, null=True)
    comment_creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_creator')
    creation_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='post')


# Polls
class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    def vote_count(self):
        return self.votes.count()


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='poll_votes')

    class Meta:
        unique_together = ('poll', 'user')