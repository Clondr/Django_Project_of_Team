from django.db import models
from django.core.exceptions import ValidationError
from core_profile.models import Profile

class Portfolio(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolio_creator')
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']
        
class PortfolioMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('file', 'Файл'),
        ('image', 'Картинка'),
        ('url', 'Посилання'),
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='portfolio_media')
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    file = models.FileField(upload_to='portfolio_files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='image')

    @property
    def extention(self):
        if self.file:
            return self.file.name.split('.')[-1].lower()
        return None
    
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    def clean(self):
        super().clean()

        if self.media_type == 'file' and self.image:
            raise ValidationError({'image':'Не можна завантажити "image" у поле "file".'})
        if self.media_type == 'image' and self.file:
            raise ValidationError({'file':'Не можна завантажити "file" у поле "image".'})


