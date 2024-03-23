from django.urls import path
from .views import EventList, EventDetail, RegisterEvent, CreateEvent, ListParticipants

urlpatterns = [
    path('events/', EventList.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetail.as_view(), name='event-detail'),
    path('register/', RegisterEvent.as_view(), name='register-event'),
    path('events/create/', CreateEvent.as_view(), name='create-event'),
    path('events/<int:event_id>/participants/',
         ListParticipants.as_view(), name='list-participants'),
]
