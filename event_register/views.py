from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Participant, Registration
from .serializers import EventSerializer, ParticipantSerializer, RegistrationSerializer
from django.utils import timezone
from django.utils.timezone import make_aware

# Create your views here.


class EventList(generics.ListAPIView):
    """View to list all events."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CreateEvent(generics.CreateAPIView):
    """View to create a new event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveAPIView):
    """View to retrieve details of a specific event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RegisterEvent(APIView):
    """View to register a participant for an event."""

    def post(self, request, *args, **kwargs):
        # Extract event_id and participant data from request
        event_id = request.data.get('event_id')
        participant_data = request.data.get('participant')

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

        event_datetime = make_aware(
            timezone.datetime.combine(event.date, event.time))

        if event_datetime < timezone.now():
            return Response({"error": "Event date or time has passed. Registration is closed."}, status=status.HTTP_400_BAD_REQUEST)

        participant_serializer = ParticipantSerializer(data=participant_data)
        if participant_serializer.is_valid():
            participant_email = participant_data['email']
            existing_participant = Participant.objects.filter(
                email=participant_email).first()
            if existing_participant:
                existing_registration = Registration.objects.filter(
                    event=event, participant=existing_participant).exists()
                if existing_registration:
                    return Response({"error": "Participant is already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    participant = existing_participant
            else:
                participant = participant_serializer.save()
        else:
            return Response(participant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        registration_data = {'event': event.id, 'participant': participant.id}
        registration_serializer = RegistrationSerializer(
            data=registration_data)
        if registration_serializer.is_valid():
            registration_serializer.save()
            return Response(registration_serializer.data, status=status.HTTP_201_CREATED)
        else:
            participant.delete()
            return Response(registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListParticipants(generics.ListAPIView):
    """View to list participants of a specific event."""
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        # Extract event_id from URL kwargs
        event_id = self.kwargs['event_id']
        registration_objects = Registration.objects.filter(event_id=event_id)
        participants_ids = registration_objects.values_list(
            'participant', flat=True)
        return Participant.objects.filter(id__in=participants_ids)
