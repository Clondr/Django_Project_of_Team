from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .forms import UploadAvatarForm, ForumPostForm
# Create your views here.

@login_required
def change_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.auto_give_role()

    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile.bio = request.POST.get('bio', profile.bio)
            if 'avatar' in request.FILES and request.FILES['avatar']:
                profile.avatar = request.FILES['avatar']
            profile.save()
            return redirect('profile')
    else:
        form = UploadAvatarForm()

    return render(request, 'profile/edit_profile.html', {'form': form, 'profile': profile})

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

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.auto_give_role()
    return render(request, 'profile/profile.html', {'profile': profile})

# Forum
@login_required
def forum(request):
    posts = ForumPost.objects.order_by('-created_at')
    return render(request, 'forum/forum.html', {'posts': posts})

@login_required
def create_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            ForumPost.objects.create(
                author=request.user,
                content=form.cleaned_data['content']
            )
            return redirect('forum')
    else:
        form = ForumPostForm()
    return render(request, 'forum/create_post.html', {'form': form})