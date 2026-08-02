from django.db import models


class ForumPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author.username}'

class ForumComment(models.Model):
    comment_title = models.CharField(max_length=255)
    comment_content = models.TextField()
    comment_image = models.FileField(upload_to='forum_comments_images/', blank=True, null=True)
    comment_creator = models.ForeignKey("core_profile.Profile", on_delete=models.CASCADE, related_name='comment_creator')
    creation_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='post')