from django.shortcuts import render, get_object_or_404, redirect
from core_events.models import *
from django.contrib.auth.decorators import login_required
from core_profile.models import Profile
from core_events.forms import *
from django.http import HttpResponseForbidden
from core_events.utils import EventCalendar
from datetime import date


def events_list(request, calendar_id):
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    
    events_list = Event.objects.filter(calendar=calendar)

    return render(request, 'events/events_list.html', {'events_list': events_list, 'calendar': calendar})

def event_detail(request, calendar_id, event_id):
    event = get_object_or_404(Event.objects.select_related('calendar', 'creator'), pk=event_id, calendar_id=calendar_id) 

    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def add_event(request, calendar_id):
    profile = request.user.profile
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    date = request.GET.get("date")

    if profile.role not in ['admin', 'moderator']:
        return HttpResponseForbidden('У вас не має на це прав!')

    if request.method == "POST":
        form = AddEventForm(request.POST)

        event_media_formset = EventMediaFormSet(request.POST, request.FILES)

        if form.is_valid() and event_media_formset.is_valid():
            event = form.save(commit=False)
            event.creator = request.user.profile
            event.calendar = calendar
            event.save()

            event_media_formset.instance = event
            event_media_formset.save()

            return redirect("events-list", calendar_id=calendar.pk)

    else:
        form = AddEventForm(initial={'date_of_start': date,})
        event_media_formset = EventMediaFormSet()

    return render(request, 
                  'events/add_event.html', 
                  {'form': form,
                   'event_media_formset': event_media_formset,
                   'profile': profile, 
                   'calendar': calendar,
                   'date': date,}
                   )

@login_required
def edit_event(request, calendar_id, event_id):
    profile = request.user.profile
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    event = get_object_or_404(Event, pk=event_id, calendar_id=calendar_id)

    if profile.role not in ['admin', 'moderator']:
        return HttpResponseForbidden('У вас не має на це прав!')
    
    if request.method == "POST":
        form = AddEventForm(
            request.POST,
            instance=event
        )

        event_media_formset = EventMediaFormSet(
            request.POST,
            request.FILES,
            instance=event
        )
        
        if form.is_valid() and event_media_formset.is_valid():
            form.save()
            event_media_formset.save()

            return redirect("event-detail", calendar_id=calendar.pk, event_id=event_id)

    else:
        form = AddEventForm(instance=event)
        event_media_formset = EventMediaFormSet(instance=event)

    return render(request, 
                  'events/edit_event.html', 
                  {'form': form,
                   'event_media_formset': event_media_formset,
                   'profile': profile,
                   'calendar': calendar,
                   'event': event}
                   )

@login_required
def delete_event(request, event_id, calendar_id):
    profile = request.user.profile
    event = get_object_or_404(Event, pk=event_id, calendar_id=calendar_id)
    calendar = get_object_or_404(Calendar, pk=calendar_id)

    if profile.role not in ['admin', 'moderator']:
        return HttpResponseForbidden('У вас не має на це прав!')
    
    if request.method == "POST":
        event.delete()

        return redirect("events-list", calendar_id=calendar.pk)

    return render(request, 
                  'events/delete_event.html', 
                  {'profile': profile,
                   'event': event,
                   'calendar': calendar}
                   )

# calendar

def calendar_events(request, calendar_id):
    calendar = get_object_or_404(Calendar, pk=calendar_id)

    today = date.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    #Вычисление предыдущих и следующих месяцов и лет.
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year 
        
    cal = EventCalendar(
        year,
        month,
        calendar,
    )

    context = {
        "calendar": calendar,
        "calendar_html": cal.formatmonth(year, month),
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }

    return render(request, 'events/calendar_events.html', context)

@login_required
def add_calendar(request):
    profile = request.user.profile

    if profile.role not in ['admin', 'moderator']:
        return HttpResponseForbidden('У вас не має на це прав!') 

    if request.method == "POST":
        name = request.POST.get('name')


        Calendar.objects.create(
            name=name
        )

        return redirect("calendars-list")

    return render(request, 'events/add_calendar.html', {'profile': profile})

@login_required
def delete_calendar(request, calendar_id):
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    profile = request.user.profile
    
    if profile.role not in ['admin', 'moderator']:
        return HttpResponseForbidden('У вас не має на це прав!') 

    if request.method == "POST":
        calendar.delete()

        return redirect("calendars-list")

    return render(request, 'events/delete_calendar.html', {'profile': profile, 'calendar': calendar})    

def calendars_list(request):
    calendars_list = Calendar.objects.all()

    return render(request, 'events/calendars_list.html', {'calendars_list': calendars_list})
