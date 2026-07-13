from django.contrib import admin
from .models import Profile, Portfolio, ForumPost, DigitalDiary, Grade

# Register your models here.
admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(ForumPost)
admin.site.register(DigitalDiary)
admin.site.register(Grade)