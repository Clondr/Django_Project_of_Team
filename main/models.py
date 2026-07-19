from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import mimetypes
from urllib.parse import urlparse, parse_qs
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

class GalleryMedia(models.Model):

    ON_CHECKING = 'on_checking'
    REJECTED = 'rejected'
    APPROVED = 'approved'

    STATUS_CHOICES = [
        (ON_CHECKING, 'On_checking'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
    ]

    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student_id')
    media = models.FileField(upload_to='gallery_images/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ON_CHECKING)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='uploader')


# Surveys
class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='surveys')
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

# ---- Materials ----
class Materials(models.Model):
    MEDIA_TYPE_CHOICES = (
       ('file', 'Файл'),
       ('youtube', 'YouTube'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='file')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def extension(self):
        if self.file:
            return self.file.name.split('.')[-1].lower()
        return None
    
    @property
    def mime_type(self):
        if self.file:
            return mimetypes.guess_type(self.file.name)[0]
        return None
    
    @property
    def youtube_embed_url(self):
        if not self.url:
            return None
        
        parsed = urlparse(self.url)
        video_id = None

        if parsed.netloc in ('youtu.be', 'www.youtu.be'):
            video_id = parsed.path.strip('/')
        elif 'youtube.com' in parsed.netloc:
            path = parsed.path.strip("/")

            if path == "watch":
                video_id = parse_qs(parsed.query).get('v', [None])[0]

            elif path.startswith('embed/'):
                video_id = path.split("/")[1]

            elif path.startswith('shorts/'):
                video_id = path.split("/")[1]
            
            elif path.startswith('live/'):
                video_id = path.split("/")[1]

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'

        return None
    
    def clean(self):
        if self.media_type == 'file':
            if not self.file:
                raise ValidationError("Для файлу потрібно його завантажити")
        
        if self.media_type == 'youtube':
            if not self.url:
                raise ValidationError("Для медіа з YouTube потрібне посилання")