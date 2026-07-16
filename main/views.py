from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import UploadAvatarForm, ForumPostForm, RegisterUserForm
from .forms import UploadAvatarForm, ForumPostForm, AddCommentForumForm
from .forms import UploadAvatarForm, CreateAdvertForm, AddGradeForm
from .forms import PollForm, PollOptionFormSet
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
        item = get_object_or_404(Item, pk=request.POST.get('item'))
        form = AddGradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.profile = profile
            grade.item = item
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

# ---- forum comments ----

def forum_comments_list(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    forum_comments_list = ForumComment.objects.filter(post=post)


    return render(request, 'forum/forum_comments/forum_comments_list.html', {'forum_comments_list': forum_comments_list, 'post': post})

def forum_comment_detail(request, forum_comment_id, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    forum_comment = get_object_or_404(ForumComment, pk=forum_comment_id)


    return render(request, 'forum/forum_comments/forum_comment_detail.html', {'forum_comment': forum_comment, 'post': post})

@login_required
def create_forum_comment(request, post_id):
    profile = request.user.profile
    post = get_object_or_404(ForumPost, pk=post_id)
    
    if request.method == "POST":
        form = AddCommentForumForm(request.POST, request.FILES)

        if form.is_valid(): 
           forum_comment = ForumComment.objects.create(
               comment_title = form.cleaned_data['comment_title'],
               comment_content = form.cleaned_data['comment_content'],
               comment_image = form.cleaned_data['comment_image'],
               comment_creator = profile,
               post = post )
           
           
        return redirect('forum-comments-list', post_id=post_id)
                                        
    else:
        form = AddCommentForumForm()

    return render(request, 'forum/forum_comments/create_forum_comment.html', {'form': form, 'post': post})

@login_required
def delete_forum_comment(request, forum_comment_id, post_id): 
    post = get_object_or_404(ForumPost, pk=post_id)
    forum_comment = get_object_or_404(ForumComment, pk=forum_comment_id)
    

    profile = request.user.profile

    if profile != forum_comment.comment_creator:
        return HttpResponseForbidden("Ви не є власником цього коментаря!")
    
    if request.method == "POST":
        forum_comment.delete()

        return redirect('forum-comments-list', post_id=post_id)
    
    return render(request, 'forum/forum_comments/forum_comment_delete_form.html', {'forum_comment': forum_comment, 'post': post})


@login_required
def edit_forum_comment(request, forum_comment_id, post_id): 
    post = get_object_or_404(ForumPost, pk=post_id)
    forum_comment = get_object_or_404(ForumComment, pk=forum_comment_id)
    profile = request.user.profile

    if profile != forum_comment.comment_creator:
        return HttpResponseForbidden("Ви не є власником цього коментаря!")

    if request.method == "POST":
        form = AddCommentForumForm(
            request.POST,
            request.FILES,
            instance=forum_comment
        )
        if form.is_valid():
            form.save()

            return redirect('forum-comment-detail', forum_comment_id=forum_comment_id, post_id=post_id)
    else:
        form = AddCommentForumForm(instance=forum_comment)

    
    return render(request, 'forum/forum_comments/forum_comment_edit_form.html', {'forum_comment': forum_comment, 'form': form, 'post': post})

# --------


# ---- polls ----
def polls_list(request):
    polls = Poll.objects.order_by('-created_at')
    return render(request, 'polls/polls_list.html', {'polls': polls})

def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    total_votes = poll.votes.count()
    user_vote = None
    if request.user.is_authenticated:
        user_vote = PollVote.objects.filter(poll=poll, user=request.user).first()
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'total_votes': total_votes,
        'user_vote': user_vote,
    })

@login_required
def poll_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    option_id = request.POST.get('option')
    if not option_id:
        return redirect('poll-detail', pk=pk)
    option = get_object_or_404(PollOption, pk=option_id, poll=poll)
    PollVote.objects.update_or_create(
        poll=poll, user=request.user,
        defaults={'option': option}
    )
    return redirect('poll-detail', pk=pk)

@login_required
def create_poll(request):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        form = PollForm(request.POST)
        formset = PollOptionFormSet(request.POST, queryset=PollOption.objects.none())
        if form.is_valid() and formset.is_valid():
            poll = form.save(commit=False)
            poll.creator = profile
            poll.save()
            for option_form in formset:
                if option_form.cleaned_data.get('text'):
                    option = option_form.save(commit=False)
                    option.poll = poll
                    option.save()
            return redirect('polls-list')
    else:
        form = PollForm()
        formset = PollOptionFormSet(queryset=PollOption.objects.none())
    return render(request, 'polls/poll_form.html', {'form': form, 'formset': formset})

@login_required
def edit_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        formset = PollOptionFormSet(request.POST, queryset=poll.options.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            for option_form in formset:
                if option_form.cleaned_data.get('DELETE'):
                    if option_form.instance.pk:
                        option_form.instance.delete()
                elif option_form.cleaned_data.get('text'):
                    option = option_form.save(commit=False)
                    option.poll = poll
                    option.save()
            return redirect('poll-detail', pk=pk)
    else:
        form = PollForm(instance=poll)
        formset = PollOptionFormSet(queryset=poll.options.all())
    return render(request, 'polls/poll_form.html', {'form': form, 'formset': formset, 'poll': poll})

@login_required
def delete_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        poll.delete()
        return redirect('polls-list')
    return render(request, 'polls/poll_delete.html', {'poll': poll})

@login_required
def list_grades(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    grades = profile.grades.all()
    return render(request, 'grades/grades_list.html', {'grades': grades, 'profile': profile})