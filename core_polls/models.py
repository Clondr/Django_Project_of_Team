from django.db import models

# Create your models here.

# Polls
class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='polls')
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

    profile_id = models.ForeignKey(
        "core_profile.Profile",
        on_delete=models.CASCADE,
        related_name='polls_gallery_media_student',
    )
    media = models.FileField(upload_to='gallery_images/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ON_CHECKING)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        "core_profile.Profile",
        on_delete=models.CASCADE,
        related_name='polls_gallery_media_uploader',
    )
