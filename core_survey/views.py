from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseForbidden
from .forms import *
# Create your views here.

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
