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

    def formatday (self ,day ,weekday ):
        if day ==0 :
            return "<td></td>"

        current_date =date (self .year ,self .month ,day )

        events =Event .objects .filter (
        calendar =self .calendar ,
        date_of_start__lte =current_date ,
        date_of_end__gte =current_date ,
        )

        events_html =""

        for event in events :
            url =reverse (
            "event-detail",
            args =[self .calendar .pk ,event .pk ]
            )

            events_html +=(
            f'<li><a href="{url }">{event .title }</a></li>'
            )

        add_url =reverse (
        'add-event',
        args =[self .calendar .pk ]
        )+f'?date={current_date }'

        return f"""
            <td>
                <a href="{add_url }">{day }</a>
                <ul>
                    {events_html }
                </ul>
            </td>
        """