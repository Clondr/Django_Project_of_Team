from calendar import HTMLCalendar 
from core_events .models import Event 
from django .urls import reverse 
from datetime import date 


class EventCalendar (HTMLCalendar ):
    def __init__ (self ,year ,month ,calendar ):
        super ().__init__ ()
        self .year =year 
        self .month =month 
        self .calendar =calendar 
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="calendar-day empty"></td>'

        current_date = date(self.year, self.month, day)

        events = Event.objects.filter(
            calendar=self.calendar,
            date_of_start__lte=current_date,
            date_of_end__gte=current_date,
        )

        events_html = ''
        for event in events:
            url = reverse('event-detail', args=[self.calendar.pk, event.pk])
            # event block for a more Google-Calendar-like appearance
            events_html += (
                f'<div class="gc-event"><a href="{url}" title="{event.title}">{event.title}</a></div>'
            )

        add_url = reverse('add-event', args=[self.calendar.pk]) + f'?date={current_date}'

        return (
            f'<td class="calendar-day">'
            f'<div class="day-number">{day}</div>'
            f'<div class="day-actions"><a href="{add_url}" class="text-decoration-none small">+</a></div>'
            f'<div class="events-list">{events_html}</div>'
            f'</td>'
        )

    def formatmonth(self, theyear, themonth, withyear=True):
        import calendar as _pycal

        month_name = _pycal.month_name[themonth]
        weekdays = list(self.iterweekdays())

        # header
        header_html = f'<div class="calendar-header"><div class="calendar-title">{month_name} {theyear}</div></div>'

        # build table
        table_html = ['<table class="gc-month table">']
        # weekday headers
        table_html.append('<thead><tr>')
        for wd in weekdays:
            table_html.append(f'<th class="gc-weekday">{_pycal.day_abbr[wd]}</th>')
        table_html.append('</tr></thead>')

        # weeks
        table_html.append('<tbody>')
        for week in self.monthdayscalendar(theyear, themonth):
            table_html.append('<tr>')
            for i, day in enumerate(week):
                wd = weekdays[i]
                table_html.append(self.formatday(day, wd))
            table_html.append('</tr>')
        table_html.append('</tbody>')
        table_html.append('</table>')

        raw = ''.join(table_html)
        return f'<div class="calendar">{header_html}<div class="calendar-table-wrap">{raw}</div></div>'