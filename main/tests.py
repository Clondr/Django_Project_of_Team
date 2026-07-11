from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class ProfileAvatarUploadTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.profile = self.user.profile
        self.client.force_login(self.user)

    def test_avatar_upload_is_saved(self):
        image = Image.new('RGB', (185, 194), color='red')
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        uploaded_file = SimpleUploadedFile(
            'avatar.png',
            image_bytes.read(),
            content_type='image/png',
        )

        response = self.client.post(
            reverse('change-profile'),
            {'bio': 'new bio', 'avatar': uploaded_file},
            format='multipart',
        )

        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.avatar)
        self.assertIn('avatars/', self.profile.avatar.name)
        self.assertTrue(self.profile.avatar.storage.exists(self.profile.avatar.name))
