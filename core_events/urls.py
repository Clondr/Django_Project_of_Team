from django .contrib import admin 
from django .urls import path 
from core_events .views import *

urlpatterns =[
path ('events-list/<int:calendar_id>/',events_list ,name ='events-list'),
path ('event-detail/<int:calendar_id>/<int:event_id>/',event_detail ,name ='event-detail'),
path ('add-event/<int:calendar_id>/',add_event ,name ='add-event'),
path ('edit-event/<int:calendar_id>/<int:event_id>/',edit_event ,name ='edit-event'),
path ('delete-event/<int:calendar_id>/<int:event_id>/',delete_event ,name ='delete-event'),

path ('calendar-events/<int:calendar_id>/',calendar_events ,name ='calendar-events'),
path ('add-calendar/',add_calendar ,name ='add-calendar'),
path ('delete-calendar/<int:calendar_id>/',delete_calendar ,name ='delete-calendar'),
path ('calendars-list/',calendars_list ,name ='calendars-list'),
]