from dataclasses import dataclass, field, asdict
from typing import Optional
import re


VALID_STATUSES = {"draft", "published", "cancelled", "completed", "active"}


def validate_string_length(value: str, field_name: str, min_len: int = None, max_len: int = None):
    """Validate string length constraints"""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    if min_len is not None and len(value) < min_len:
        raise ValueError(f"{field_name} must be at least {min_len} characters")
    if max_len is not None and len(value) > max_len:
        raise ValueError(f"{field_name} must be at most {max_len} characters")


def validate_status(value: str):
    """Validate status field"""
    if value not in VALID_STATUSES:
        raise ValueError(f"status must be one of: {', '.join(VALID_STATUSES)}")


def validate_capacity(value: int):
    """Validate capacity field"""
    if not isinstance(value, int):
        raise ValueError("capacity must be an integer")
    if value <= 0:
        raise ValueError("capacity must be greater than 0")


@dataclass
class EventCreate:
    title: str
    description: str
    date: str
    location: str
    capacity: int
    organizer: str
    status: str
    eventId: Optional[str] = None
    
    def __post_init__(self):
        """Validate fields after initialization"""
        validate_string_length(self.title, "title", min_len=1, max_len=200)
        validate_string_length(self.description, "description", max_len=1000)
        validate_string_length(self.date, "date", min_len=1)
        validate_string_length(self.location, "location", min_len=1, max_len=200)
        validate_capacity(self.capacity)
        validate_string_length(self.organizer, "organizer", min_len=1, max_len=100)
        validate_status(self.status)
    
    def dict(self):
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class EventUpdate:
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    organizer: Optional[str] = None
    status: Optional[str] = None
    
    def __post_init__(self):
        """Validate fields after initialization"""
        if self.title is not None:
            validate_string_length(self.title, "title", min_len=1, max_len=200)
        if self.description is not None:
            validate_string_length(self.description, "description", max_len=1000)
        if self.date is not None:
            validate_string_length(self.date, "date", min_len=1)
        if self.location is not None:
            validate_string_length(self.location, "location", min_len=1, max_len=200)
        if self.capacity is not None:
            validate_capacity(self.capacity)
        if self.organizer is not None:
            validate_string_length(self.organizer, "organizer", min_len=1, max_len=100)
        if self.status is not None:
            validate_status(self.status)
    
    def dict(self, exclude_unset: bool = False):
        """Convert to dictionary, optionally excluding None values"""
        data = asdict(self)
        if exclude_unset:
            return {k: v for k, v in data.items() if v is not None}
        return data


@dataclass
class Event:
    eventId: str
    title: str
    description: str
    date: str
    location: str
    capacity: int
    organizer: str
    status: str
    createdAt: str
    updatedAt: str
    
    def dict(self):
        """Convert to dictionary"""
        return asdict(self)
