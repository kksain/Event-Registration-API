## Event Registration API
Overview
The Event Registration API is a Django-based backend solution developed using Django and Django REST Framework.
It provides functionality for managing events and allowing participants to register for upcoming events.
The API follows RESTful principles, ensuring clear API design and efficient data modeling.

## Features
-Event Management: Create, update, and delete events with details such as name, description, date, and time.
-Participant Registration: Users can register for events by providing their name and email. Email validation and uniqueness checks are enforced.
-Event Listing: Endpoints to list all available events and retrieve detailed information about specific events.
-Prevent Registration for Past Events: Registration is automatically closed for events whose date or time has passed.
-Data Integrity: Efficient use of Django models and relationships to ensure data integrity and facilitate querying.

## Create and Activate Virtual Environment:
python -m venv env
source env/bin/activate


## Installation
Clone the repository:
-git clone https://github.com/kksain/Event-Registration-API/
-Navigate to the project directory:cd event_registration

## Install dependencies:
pip install -r requirements.txt

## Apply migrations:
python manage.py migrate

## Run the development server:
python manage.py runserver


## API Endpoints
-List Events:
Endpoint: GET /events/
Description: This endpoint lists all available events.
Example Usage: GET http://127.0.0.1:800/events/

-Event Detail:
Endpoint: GET /events/<event_id>/
Description: This endpoint retrieves details of a specific event identified by its ID.
Example Usage: GET http://127.0.0.1:8000/events/1/ (Replace 1 with the actual event ID)

-Register Event:
Endpoint: POST http://127.0.0.1:8000/register/
Description: This endpoint allows a user to register for an event by providing event ID and participant details.
Example Usage:
POST http://127.0.0.1:8000/register/
Content-Type: application/json

{
    "event_id": 1,
    "participant": {
        "name": "kk sain",
        "email": "kt841719@gmail.com"
    }
}

-Create Event:
Endpoint: POST http://127.0.0.1:8000/events/create/
Description: This endpoint allows event organizers to create a new event by providing event details.
Example Usage:
POST http://127.0.0.1:8000/events/create/
Content-Type: application/json
{
    "name": "New Year's Eve Party",
    "description": "Celebrate the arrival of the new year with friends and family.",
    "date": "2024-12-31",
    "time": "20:00:00"
}

-List Participants:
Endpoint: GET http://127.0.0.1:8000/events/<event_id>/participants/
Description: This endpoint lists all participants registered for a specific event identified by its ID.
Example Usage: GET http://127.0.0.1:8000/events/1/participants/ (Replace 1 with the actual event ID)

## Testing
Use Postman or any API testing tool to test the API endpoints. You can import the provided Postman collection to quickly get started with testing.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to contribute to the project.
