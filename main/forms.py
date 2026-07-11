from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField(label='Завантажити аватар', required=False)

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