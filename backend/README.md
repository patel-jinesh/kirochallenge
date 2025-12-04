# Events API Backend

FastAPI REST API for managing events with DynamoDB storage.

## Features

- Full CRUD operations for events
- DynamoDB integration
- Input validation with Pydantic
- CORS support
- OpenAPI documentation

## Event Properties

- `eventId`: Unique identifier (auto-generated UUID)
- `title`: Event title
- `description`: Event description
- `date`: Event date (ISO format: YYYY-MM-DD)
- `location`: Event location
- `capacity`: Maximum number of attendees
- `organizer`: Event organizer name
- `status`: Event status (draft, published, cancelled, completed)
- `createdAt`: Creation timestamp (auto-generated)
- `updatedAt`: Last update timestamp (auto-generated)

## Setup

1. Create virtual environment and install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS configuration
```

3. Ensure DynamoDB table exists (or use infrastructure/CDK to deploy)

## Run

```bash
uvicorn main:app --reload
```

API will be available at http://localhost:8000

## API Endpoints

- `POST /events` - Create a new event
- `GET /events` - List all events
- `GET /events/{event_id}` - Get a specific event
- `PUT /events/{event_id}` - Update an event
- `DELETE /events/{event_id}` - Delete an event
- `GET /health` - Health check

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Request

```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-06-15",
    "location": "San Francisco, CA",
    "capacity": 500,
    "organizer": "Tech Events Inc",
    "status": "published"
  }'
```
