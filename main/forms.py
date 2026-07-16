from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Advertisement, Grade, ForumComment, Poll, PollOption, Item, GalleryMedia, Survey, SurveyPage, SurveyQuestion, SurveyQuestionOption
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User

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
    

class ForumPostForm(forms.Form):
    content = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 10:
            raise ValidationError('Повідомлення повинно містити мінімум 10 символів.')
        return content


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

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

class CreateAdvertForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['advert_title', 'content', 'content_image']
        widgets = {
            'advert_title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'item', ]

class AddCommentForumForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['comment_title', 'comment_content', 'comment_image']
        widgets = {
            'comment_title': forms.TextInput(attrs={'class': 'form-control'}),
            'comment_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'comment_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

PollOptionFormSet = forms.modelformset_factory(
    PollOption,
    fields=['text'],
    widgets={'text': forms.TextInput(attrs={'class': 'form-control'})},
    extra=3,
    can_delete=True,
)

class GalleryMediaUploadForm(forms.ModelForm):

    class Meta:
        model = GalleryMedia
        fields = ['media',]

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SurveyPageForm(forms.ModelForm):
    class Meta:
        model = SurveyPage
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва сторінки (опціонально)'}),
        }

class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ['text', 'question_type']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
        }
