from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

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
