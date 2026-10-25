# EventHub - Event Ticketing Backend API

## Overview

EventHub is a backend API built using Django and Django REST Framework (DRF) for managing events and seat reservations.

Users can:

- Browse events
- Reserve seats for events
- Cancel reservations
- Filter events and reservations

The application automatically updates event seat availability when reservations are created or cancelled.

## Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- SQLite3

## Features

### Event Management

- Create events
- Retrieve all events
- Retrieve a specific event
- Update events
- Delete events
- Filter events by status
- Filter events by venue

### Reservation Management

- Create reservations
- Retrieve reservations
- Filter reservations by event
- Prevent overbooking
- Cancel reservations
- Automatically restore seats after cancellation

### Middleware

- Logs request method
- Logs request path
- Logs response status code
- Logs request execution time

## Project Structure

```text
eventhub/
├── manage.py
├── db.sqlite3
├── README.md
├── requirements.txt
├── eventhub/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── events/
    ├── admin.py
    ├── middleware.py
    ├── models.py
    ├── serializer.py
    ├── urls.py
    ├── views.py
    └── migrations/
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
```

### 2. Move Into the Project Directory

```bash
cd eventhub
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### Event Endpoints

#### Create an Event

```http
POST /api/events/
```

#### List All Events

```http
GET /api/events/
```

#### Retrieve a Single Event

```http
GET /api/events/{id}/
```

#### Update an Entire Event

```http
PUT /api/events/{id}/
```

#### Partially Update an Event

```http
PATCH /api/events/{id}/
```

#### Delete an Event

```http
DELETE /api/events/{id}/
```

#### Filter Events by Status

```http
GET /api/events/?status=upcoming
```

#### Filter Events by Venue

```http
GET /api/events/?venue=Bangalore
```

### Reservation Endpoints

#### Create a Reservation

```http
POST /api/reservations/
```

#### List All Reservations

```http
GET /api/reservations/
```

#### Retrieve a Single Reservation

```http
GET /api/reservations/{id}/
```

#### Filter Reservations by Event

```http
GET /api/reservations/?event_id=1
```

#### Cancel a Reservation

```http
POST /api/reservations/{id}/cancel/
```

No request body is required for cancellation.

## Sample API Requests

### Create an Event

```json
{
  "title": "PyCon India 2026",
  "venue": "Bangalore",
  "date": "2026-12-20",
  "total_seats": 500,
  "available_seats": 500,
  "status": "upcoming"
}
```

### Create a Reservation

```json
{
  "event": 1,
  "attend_name": "Priya Sharma",
  "email": "priya@example.com",
  "seats_reserved": 2
}
```

## Validation Rules

### Event Validation

- Event title is mandatory.
- Event venue is mandatory.
- Event date is mandatory.
- Available seats cannot exceed total seats.

### Reservation Validation

- At least one seat must be reserved.
- Reservations can be created only for upcoming or ongoing events.
- The requested number of seats cannot exceed the available seats.
- Attendee name is mandatory.
- Email is mandatory.
- An already cancelled reservation cannot be cancelled again.

## Design Decision

The Event model stores both `total_seats` and `available_seats`.

Instead of calculating available seats from all confirmed reservations whenever an event is retrieved, the application updates `available_seats` when a reservation is created or cancelled.

This design was chosen because it:

- Makes seat availability checks straightforward.
- Avoids recalculating availability during every event request.
- Keeps reservation and cancellation logic easy to understand for this project.

When a reservation is created, the reserved seat count is deducted from `available_seats`. When the reservation is cancelled, the same number of seats is added back.

## Request Logging Middleware

The project includes custom middleware that records:

- HTTP request method
- Request path
- Response status code
- Processing time

Example terminal output:

```text
GET /api/events/ - 200 - 0.01s
POST /api/reservations/ - 201 - 0.03s
POST /api/reservations/1/cancel/ - 200 - 0.02s
```

## Testing Checklist

- [x] Create an event
- [x] List all events
- [x] Filter events by status
- [x] Filter events by venue
- [x] Create a reservation and deduct seats
- [x] Reject an overbooking attempt with HTTP 400
- [x] Cancel a reservation and restore seats
- [x] Reject a repeated cancellation
- [x] Filter reservations by event ID
- [x] Display middleware logs for API requests

## Required Postman Screenshots

The submission should include screenshots showing:

1. Successful reservation with `201 Created`
2. Overbooking failure with `400 Bad Request`
3. Successful reservation cancellation

## Author

**Suganthan T H**
