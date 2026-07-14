from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import UploadAvatarForm, ForumPostForm, RegisterUserForm
from .forms import UploadAvatarForm, ForumPostForm
from .forms import UploadAvatarForm, CreateAdvertForm, AddGradeForm
from django.db.models import Avg


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

# auth
def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterUserForm()
    return render(request, 'auth_system/register.html', context={'form': form})

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
    average_score = profile.grades.aggregate(avg_score=Avg('score'))['avg_score']
    profile.auto_give_role()
    return render(request, 'profile/profile.html', {'profile': profile, 'average_score': average_score})

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

@login_required
def edit_forum_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('forum')
    else:
        form = ForumPostForm(initial={'content': post.content})
    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_forum_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        post.delete()
        return redirect('forum')
    return render(request, 'forum/delete_post.html', {'post': post})

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

@login_required
def add_grade(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method == 'POST':
        form = AddGradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.profile = profile
            grade.save()
            return redirect('profile-detail', profile_id=profile.id)
    else:
        form = AddGradeForm()

    return render(request, 'grades/grade_creation_form.html', {'form': form, 'profile': profile})

def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    average_score = profile.grades.aggregate(avg_score=Avg('score'))['avg_score']
    profile.auto_give_role()
    return render(request, 'profile/profile_detail.html', {'profile': profile, 'average_score': average_score})
