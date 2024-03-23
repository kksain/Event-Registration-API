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
            # Retrieve the event object using the provided event_id
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            # Return 404 error if event does not exist
            return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Convert event datetime to aware datetime object
        event_datetime = make_aware(
            timezone.datetime.combine(event.date, event.time))

        # Check if event datetime has passed
        if event_datetime < timezone.now():
            # Return error if event has already passed
            return Response({"error": "Event date or time has passed. Registration is closed."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate participant data using ParticipantSerializer
        participant_serializer = ParticipantSerializer(data=participant_data)
        if participant_serializer.is_valid():
            # If participant data is valid, extract participant email
            participant_email = participant_data['email']
            # Check if participant with the same email exists
            existing_participant = Participant.objects.filter(
                email=participant_email).first()
            if existing_participant:
                # If participant exists, check if already registered for the event
                existing_registration = Registration.objects.filter(
                    event=event, participant=existing_participant).exists()
                if existing_registration:
                    # Return error if participant is already registered for the event
                    return Response({"error": "Participant is already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # If not registered, use existing participant
                    participant = existing_participant
            else:
                # If participant does not exist, create a new one
                participant = participant_serializer.save()
        else:
            # Return validation errors if participant data is invalid
            return Response(participant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create registration data with event and participant IDs
        registration_data = {'event': event.id, 'participant': participant.id}
        # Validate registration data using RegistrationSerializer
        registration_serializer = RegistrationSerializer(
            data=registration_data)
        if registration_serializer.is_valid():
            # If registration data is valid, save the registration
            registration_serializer.save()
            # Return registration data with 201 status code
            return Response(registration_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If registration data is invalid, delete the participant and return errors
            participant.delete()
            return Response(registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListParticipants(generics.ListAPIView):
    """View to list participants of a specific event."""
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        # Extract event_id from URL kwargs
        event_id = self.kwargs['event_id']
        # Filter registration objects based on event_id
        registration_objects = Registration.objects.filter(event_id=event_id)
        # Get participant IDs from registration objects
        participants_ids = registration_objects.values_list(
            'participant', flat=True)
        # Return participants queryset filtered by participant IDs
        return Participant.objects.filter(id__in=participants_ids)
