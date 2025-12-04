from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from dotenv import load_dotenv

from models import Event, EventCreate, EventUpdate
from database import db_client

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Events API",
    description="REST API for managing events with DynamoDB",
    version="1.0.0"
)


# Custom exception handler for validation errors
@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Events API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(request: Request):
    """Create a new event"""
    try:
        body = await request.json()
        event = EventCreate(**body)
        event_data = event.dict()
        created_event = db_client.create_event(event_data)
        return created_event
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events")
def list_events(status: str = None):
    """Get all events, optionally filtered by status"""
    try:
        events = db_client.list_events(status_filter=status)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events/{event_id}")
def get_event(event_id: str):
    """Get a specific event by ID"""
    try:
        event = db_client.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/events/{event_id}")
async def update_event(event_id: str, request: Request):
    """Update an event"""
    try:
        # Check if event exists
        existing_event = db_client.get_event(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Update event
        body = await request.json()
        event_update = EventUpdate(**body)
        update_data = event_update.dict(exclude_unset=True)
        updated_event = db_client.update_event(event_id, update_data)
        return updated_event
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    """Delete an event"""
    try:
        # Check if event exists
        existing_event = db_client.get_event(event_id)
        if not existing_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        db_client.delete_event(event_id)
        return {"message": "Event deleted successfully", "eventId": event_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
