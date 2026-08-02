from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from core_forum.models import *
from core_forum.forms import *
from django.contrib.auth.decorators import login_required


# ---- forum ----
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
# -------- 

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