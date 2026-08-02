from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField(
        label='Завантажити аватар',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Получаем ширину и высоту изображения
            width, height = get_image_dimensions(avatar)
            
            # Строгая проверка на размеры 185 x 194
            if width != 185 or height != 194:
                raise ValidationError(
                    f"Розширення може бути тільки 185x194 пікселей. "
                    f"Розмір: {width}x{height}."
                )
        return avatar

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваше ім\'я (опціонально)'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваше прізвище (опціонально)'})
    )
    email = forms.EmailField(
        required=False,
        help_text='Опціональне поле. Якщо вказати, буде надіслано листа для активації.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть вашу електронну пошту (опціонально)'})
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')