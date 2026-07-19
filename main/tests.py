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


class RegistrationTests(TestCase):
    def test_registration_logs_in_user_and_redirects_to_profile(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
                'first_name': '',
                'last_name': '',
            },
        )

        user = get_user_model().objects.get(username='newuser')

        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertTrue(user.is_authenticated)


class WelcomeBannerTests(TestCase):
    def test_welcome_banner_is_rendered_for_first_time_visitor(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Раді бачити вас!')
        self.assertContains(response, 'id="welcome-banner"')

    def test_accept_offer_sets_cookie_and_hides_banner(self):
        self.client.post(reverse('accept_offer'))

        self.assertEqual(self.client.cookies['site_offer_accepted'].value, 'true')

        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'id="welcome-banner"')
