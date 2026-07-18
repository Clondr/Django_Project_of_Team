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
from .forms import PollForm, PollOptionFormSet, GalleryMediaUploadForm, SurveyForm, SurveyPageForm, SurveyQuestionForm
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

@login_required
def change_detail_profile(request, pk):
    profile = get_object_or_404(Profile, user=request.user, pk=pk)
    profile.auto_give_role()

    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile.bio = request.POST.get('bio', profile.bio)
            if 'avatar' in request.FILES and request.FILES['avatar']:
                profile.avatar = request.FILES['avatar']
            profile.save()
            return redirect('profile-detail', pk=pk)
    else:
        form = UploadAvatarForm()

    return render(request, 'profile/edit_detail_profile.html', {'form': form, 'profile': profile})

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
def add_grade(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = AddGradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.profile = profile
            grade.save()
            return redirect('profile-detail', pk=pk)
    else:
        form = AddGradeForm()

    return render(request, 'grades/grade_creation_form.html', {'form': form, 'profile': profile})

@login_required
def list_grades(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    grades = profile.grades.all()
    return render(request, 'grades/grades_list.html', {'grades': grades, 'profile': profile})

@login_required
def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)

    if request.method == 'POST':
        form = AddGradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('list-grades', pk=grade.profile.pk)
    else:
        form = AddGradeForm(instance=grade)

    return render(request, 'grades/grades_edit.html', {'form': form, 'grade': grade})

@login_required
def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)

    if request.method == 'POST':
        grade.delete()

        return redirect('list-grades', pk=grade.profile.pk)
    
    return render(request, 'grades/grades_delete_confirm.html', {'grade': grade})



def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
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

# ---- gallery ----

def gallery_media_list(request):
    media_list = GalleryMedia.objects.filter(status=GalleryMedia.APPROVED)
    return render(request, 'gallery/gallery_list.html', {'media_list': media_list, 'profile': request.user.profile})

@login_required
def moderation_gallery(request):
    profile = request.user.profile
    if profile.role not in ['moderator', 'admin']:
        return HttpResponseForbidden('У вас не має на це прав!')
    media_list = GalleryMedia.objects.filter(status=GalleryMedia.ON_CHECKING)
    return render(request, 'gallery/moderation_gallery.html', {'media_list': media_list})

@login_required
def upload_to_gallery(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        form = GalleryMediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            GalleryMedia.objects.create(
                profile_id=profile,
                media=form.cleaned_data['media'],
                uploaded_by=request.user.profile
            )
            return redirect('gallery-list')
    else:
        form = GalleryMediaUploadForm()
    return render(request, 'gallery/add_media.html', {'form': form, 'profile': profile})

@login_required
def approve_addition(request, media_id):
    if request.method != "POST":
        return HttpResponseForbidden()
    profile = request.user.profile
    if profile.role not in ['moderator', 'admin']:
        return HttpResponseForbidden("У вас не має на це прав!")
    media = get_object_or_404(GalleryMedia, id=media_id)
    media.status = GalleryMedia.APPROVED
    media.save()
    return redirect('gallery-list')

# ---- surveys ----
def surveys_list(request):
    surveys = Survey.objects.order_by('-created_at')
    return render(request, 'surveys/surveys_list.html', {'surveys': surveys})

@login_required
def survey_take(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    pages = list(survey.pages.all())
    if not pages:
        return redirect('surveys-list')

    page_index = int(request.GET.get('page', 0))
    if page_index >= len(pages):
        return redirect('survey-results-user', pk=pk)

    current_page = pages[page_index]
    questions = current_page.questions.all()

    if request.method == 'POST':
        # Зберігаємо або оновлюємо відповідь
        response, _ = SurveyResponse.objects.get_or_create(survey=survey, user=request.user)
        for question in questions:
            if question.question_type == SurveyQuestion.TEXT:
                answer_text = request.POST.get(f'q_{question.pk}', '')
                SurveyAnswer.objects.update_or_create(
                    response=response, question=question,
                    defaults={'text_answer': answer_text, 'choice_answer': None}
                )
            else:
                option_id = request.POST.get(f'q_{question.pk}')
                if option_id:
                    option = get_object_or_404(SurveyQuestionOption, pk=option_id)
                    SurveyAnswer.objects.update_or_create(
                        response=response, question=question,
                        defaults={'choice_answer': option, 'text_answer': ''}
                    )

        next_index = page_index + 1
        if next_index < len(pages):
            return redirect(f"{request.path}?page={next_index}")
        return redirect('survey-results-user', pk=pk)

    # Підтягуємо попередні відповіді якщо є
    existing_answers = {}
    if SurveyResponse.objects.filter(survey=survey, user=request.user).exists():
        response = SurveyResponse.objects.get(survey=survey, user=request.user)
        for ans in response.answers.filter(question__page=current_page):
            existing_answers[ans.question_id] = ans

    return render(request, 'surveys/survey_take.html', {
        'survey': survey,
        'current_page': current_page,
        'questions': questions,
        'page_index': page_index,
        'total_pages': len(pages),
        'existing_answers': existing_answers,
    })

@login_required
def survey_results_user(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    response = get_object_or_404(SurveyResponse, survey=survey, user=request.user)
    answers = response.answers.select_related('question', 'choice_answer')
    return render(request, 'surveys/survey_results_user.html', {
        'survey': survey, 'answers': answers
    })

@login_required
def survey_results_admin(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    survey = get_object_or_404(Survey, pk=pk)
    pages = survey.pages.prefetch_related('questions__options').all()
    total_responses = survey.responses.count()

    stats = []
    for page in pages:
        for question in page.questions.all():
            if question.question_type == SurveyQuestion.CHOICE:
                options_stats = []
                for option in question.options.all():
                    count = SurveyAnswer.objects.filter(question=question, choice_answer=option).count()
                    options_stats.append({'option': option, 'count': count})
                stats.append({'question': question, 'type': 'choice', 'options': options_stats})
            else:
                answers = SurveyAnswer.objects.filter(question=question).exclude(text_answer='')
                stats.append({'question': question, 'type': 'text', 'answers': answers})

    return render(request, 'surveys/survey_results_admin.html', {
        'survey': survey, 'stats': stats, 'total_responses': total_responses
    })

@login_required
def create_survey(request):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = profile
            survey.save()
            return redirect('edit-survey', pk=survey.pk)
    else:
        form = SurveyForm()
    return render(request, 'surveys/survey_form.html', {'form': form})

@login_required
def edit_survey(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyForm(request.POST or None, instance=survey)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('edit-survey', pk=pk)
    pages = survey.pages.prefetch_related('questions__options').all()
    return render(request, 'surveys/survey_edit.html', {'survey': survey, 'form': form, 'pages': pages})

@login_required
def add_survey_page(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    survey = get_object_or_404(Survey, pk=pk)
    order = survey.pages.count()
    page = SurveyPage.objects.create(survey=survey, order=order)
    return redirect('edit-survey-page', pk=page.pk)

@login_required
def edit_survey_page(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    page = get_object_or_404(SurveyPage, pk=pk)
    page_form = SurveyPageForm(request.POST or None, instance=page)
    if request.method == 'POST' and page_form.is_valid():
        page_form.save()

        # Зберігаємо питання
        question_ids = request.POST.getlist('question_ids')
        for qid in question_ids:
            q = get_object_or_404(SurveyQuestion, pk=qid)
            q.text = request.POST.get(f'q_text_{qid}', q.text)
            q.question_type = request.POST.get(f'q_type_{qid}', q.question_type)
            q.save()
            # Зберігаємо варіанти
            option_ids = request.POST.getlist(f'option_ids_{qid}')
            for oid in option_ids:
                opt = get_object_or_404(SurveyQuestionOption, pk=oid)
                opt.text = request.POST.get(f'opt_text_{oid}', opt.text)
                opt.save()
            # Нові варіанти
            new_options = request.POST.getlist(f'new_options_{qid}')
            for opt_text in new_options:
                if opt_text.strip():
                    SurveyQuestionOption.objects.create(question=q, text=opt_text.strip())

        # Нові питання
        new_questions = request.POST.getlist('new_question_text')
        new_types = request.POST.getlist('new_question_type')
        for i, text in enumerate(new_questions):
            if text.strip():
                q_type = new_types[i] if i < len(new_types) else SurveyQuestion.TEXT
                q = SurveyQuestion.objects.create(page=page, text=text.strip(), question_type=q_type, order=page.questions.count())
                new_opts = request.POST.getlist(f'new_question_options_{i}')
                for opt_text in new_opts:
                    if opt_text.strip():
                        SurveyQuestionOption.objects.create(question=q, text=opt_text.strip())

        return redirect('edit-survey-page', pk=pk)

    return render(request, 'surveys/survey_page_edit.html', {'page': page, 'page_form': page_form})

@login_required
def delete_survey_page(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    page = get_object_or_404(SurveyPage, pk=pk)
    survey_pk = page.survey.pk
    page.delete()
    return redirect('edit-survey', pk=survey_pk)

@login_required
def delete_survey_question(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    question = get_object_or_404(SurveyQuestion, pk=pk)
    page_pk = question.page.pk
    question.delete()
    return redirect('edit-survey-page', pk=page_pk)

@login_required
def delete_survey(request, pk):
    profile = request.user.profile
    if profile.role not in ('moderator', 'admin'):
        return HttpResponseForbidden('У вас немає на це прав!')
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == 'POST':
        survey.delete()
        return redirect('surveys-list')
    return render(request, 'surveys/survey_delete.html', {'survey': survey})
