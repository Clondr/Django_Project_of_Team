from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from datetime import date

@csrf_protect
@require_POST
def accept_offer(request):
    response = redirect('home')
    response.set_cookie(
        'site_offer_accepted',
        'true',
        max_age=60 * 60 * 24 * 30,
        httponly=False,
        samesite='Lax',
    )
    request.session['banner_shown'] = True
    return response


# auth
def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            
            user.is_active = True
            user.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            
            # Якщо є email - відправляємо листа активації
            if email:
                # Генерируем токен активации
                token = account_activation_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Строим ссылку активации
                activation_link = request.build_absolute_uri(
                    reverse('activate-account', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Подготавливаем контекст для шаблона email
                context = {
                    'username': user.username,
                    'activation_link': activation_link,
                }
                
                # Отправляем HTML email
                subject = 'Активація вашого облікового запису'
                
                # Создаем сообщение
                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=f'Активуйте аккаунт по посиланню: {activation_link}',
                    from_email='bkirilleb09@gmail.com',
                    to=[user.email]
                )
                
                # Добавляем HTML версию
                html_content = render_to_string('auth_system/activation_email.html', context)
                email_message.attach_alternative(html_content, "text/html")
                
                try:
                    email_message.send()
        
                except Exception as e:
                    pass
            
            return redirect('profile')
    else:
        form = RegisterUserForm()
    return render(request, 'auth_system/register.html', context={'form': form})

def activate_account(request, uidb64, token):
    """Активирует аккаунт пользователя по токену из email"""
    try:
        # Декодируем UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Проверяем наличие email - активировать можна лише якщо є email
    if user is not None and user.email and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('profile')
    else:
        pass

def login_view(request): 
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm(request)

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'auth_system/login.html', {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# adverts
@login_required
def add_advert(request):
    profile = request.user.profile

    if profile.role == 'moderator' or profile.role == 'admin':
        if request.method == 'POST':
            form = CreateAdvertForm(request.POST, request.FILES)
            if form.is_valid(): 
                advert = Advertisement.objects.create(
                    advert_title=form.cleaned_data['advert_title'],
                    content=form.cleaned_data['content'],
                    content_image=form.cleaned_data['content_image'],
                    creator=request.user.profile,
                )
                

                return redirect('adverts-list')
        else:
            form = CreateAdvertForm()
            
        return render(request, 'adverts/advert_creation_form.html', {'form': form})
    
    return HttpResponseForbidden("Ви не маєте на це прав!")

def advert_detail(request, pk):
    advert = get_object_or_404(Advertisement, pk=pk)

    return render(request, 'adverts/advert_detail.html', {'advert': advert})

def advert_list(request):
    adverts_list = Advertisement.objects.all()

    return render(request, 'adverts/adverts_list.html', {'adverts_list': adverts_list})

@login_required
def update_advert(request, pk):
    advert = get_object_or_404(Advertisement, pk=pk)

    
    profile = request.user.profile

    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')

    else:
        if request.method == "POST":
            form = CreateAdvertForm(
                request.POST,
                request.FILES,
                instance=advert
            )

            if form.is_valid():
                form.save()

                return redirect('advert-detail', pk=advert.pk)
        else:
            form = CreateAdvertForm(instance=advert)

    return render(request, 'adverts/update_advert_form.html', {'form': form, 'advert': advert})

@login_required
def delete_advert(request, pk):
    advert = get_object_or_404(Advertisement, pk=pk)

    profile = request.user.profile

    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')

    if request.method == 'POST':
        advert.delete()

        return redirect('adverts-list')
    
    return render(request, 'adverts/delete_advert.html', {'advert': advert})


def home(request):
    return render(request, 'home.html')