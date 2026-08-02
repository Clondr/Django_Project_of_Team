from django.db import models
from django.core.exceptions import ValidationError
import mimetypes
from urllib.parse import urlparse, parse_qs


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
            