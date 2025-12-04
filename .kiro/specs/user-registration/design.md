# Design Document: User Registration System

## Overview

The user registration system extends the existing FastAPI/DynamoDB backend to manage users and event registrations with capacity constraints and waitlist functionality. The system will maintain data integrity while handling concurrent operations and provide a RESTful API for user and registration management.

The design leverages the existing infrastructure (FastAPI, DynamoDB, AWS Lambda) and follows the established patterns in the codebase for consistency.

## Architecture

### High-Level Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│         FastAPI Application         │
│  ┌─────────────────────────────┐   │
│  │   API Endpoints Layer       │   │
│  │  - User Management          │   │
│  │  - Event Registration       │   │
│  │  - Registration Queries     │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Business Logic Layer      │   │
│  │  - Registration Manager     │   │
│  │  - Waitlist Manager         │   │
│  │  - Validation Logic         │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Data Access Layer         │   │
│  │  - DynamoDB Client          │   │
│  │  - Transaction Handling     │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │   DynamoDB   │
        │   - Users    │
        │   - Events   │
        │   - Registr. │
        └──────────────┘
```

### Data Storage Strategy

We'll use DynamoDB with the following table design approach:

**Single Table Design** with composite keys to support efficient queries:
- Primary Key: `PK` (Partition Key), `SK` (Sort Key)
- GSI1: `GSI1PK`, `GSI1SK` for reverse lookups

This allows us to:
1. Store Users, Events, and Registrations in one table
2. Query registrations by user or by event efficiently
3. Maintain ACID properties using DynamoDB transactions

## Components and Interfaces

### 1. Data Models

#### User Model
```python
@dataclass
class User:
    userId: str          # Unique identifier
    name: str           # User's name
    createdAt: str      # ISO timestamp
    updatedAt: str      # ISO timestamp
```

#### Event Model (Extended)
```python
@dataclass
class Event:
    eventId: str
    title: str
    description: str
    date: str
    location: str
    capacity: int           # Maximum registrations
    hasWaitlist: bool       # Whether waitlist is enabled
    registeredCount: int    # Current registration count
    organizer: str
    status: str
    createdAt: str
    updatedAt: str
```

#### Registration Model
```python
@dataclass
class Registration:
    userId: str
    eventId: str
    status: str          # "registered" or "waitlisted"
    position: int        # Position in waitlist (0 for registered)
    registeredAt: str    # ISO timestamp
```

### 2. API Endpoints

#### User Management
- `POST /users` - Create a new user
- `GET /users/{userId}` - Get user details
- `GET /users` - List all users

#### Event Management (Extended)
- Extend existing `POST /events` to include `hasWaitlist` field
- Extend existing event model to track `registeredCount`

#### Registration Management
- `POST /events/{eventId}/register` - Register user for event
  - Body: `{"userId": "string"}`
  - Returns: Registration status (registered/waitlisted)
- `DELETE /events/{eventId}/register/{userId}` - Unregister user
- `GET /users/{userId}/registrations` - List user's registered events
- `GET /events/{eventId}/registrations` - List event registrations
- `GET /events/{eventId}/waitlist` - List event waitlist

### 3. Business Logic Components

#### RegistrationManager
Handles registration operations with capacity and waitlist logic:
- `register_user(user_id, event_id)` - Register user or add to waitlist
- `unregister_user(user_id, event_id)` - Remove registration and promote from waitlist
- `get_user_registrations(user_id)` - Get all registered events for user
- `get_event_registrations(event_id)` - Get all registrations for event

#### WaitlistManager
Manages waitlist operations:
- `add_to_waitlist(user_id, event_id)` - Add user to waitlist
- `remove_from_waitlist(user_id, event_id)` - Remove user from waitlist
- `promote_from_waitlist(event_id)` - Move first waitlisted user to registered
- `get_waitlist_position(user_id, event_id)` - Get user's position in waitlist

### 4. Data Access Layer

#### DynamoDB Schema

**Item Types:**

1. **User Item**
   - PK: `USER#{userId}`
   - SK: `METADATA`
   - Attributes: userId, name, createdAt, updatedAt

2. **Event Item** (existing, extended)
   - PK: `EVENT#{eventId}`
   - SK: `METADATA`
   - Attributes: eventId, title, capacity, hasWaitlist, registeredCount, ...

3. **Registration Item**
   - PK: `EVENT#{eventId}`
   - SK: `REG#{status}#{position}#{userId}`
   - GSI1PK: `USER#{userId}`
   - GSI1SK: `REG#{eventId}`
   - Attributes: userId, eventId, status, position, registeredAt

**Access Patterns:**
1. Get user by ID: Query PK=`USER#{userId}`, SK=`METADATA`
2. Get event registrations: Query PK=`EVENT#{eventId}`, SK begins_with `REG#registered`
3. Get event waitlist: Query PK=`EVENT#{eventId}`, SK begins_with `REG#waitlisted`
4. Get user's registrations: Query GSI1 where GSI1PK=`USER#{userId}`
5. Check if user registered: Query PK=`EVENT#{eventId}`, SK contains userId

## Data Models

### DynamoDB Item Structures

```python
# User Item
{
    "PK": "USER#user123",
    "SK": "METADATA",
    "userId": "user123",
    "name": "John Doe",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
}

# Event Item (extended)
{
    "PK": "EVENT#event456",
    "SK": "METADATA",
    "eventId": "event456",
    "title": "Tech Conference",
    "capacity": 100,
    "hasWaitlist": true,
    "registeredCount": 95,
    ...existing fields...
}

# Registration Item (registered)
{
    "PK": "EVENT#event456",
    "SK": "REG#registered#0000#user123",
    "GSI1PK": "USER#user123",
    "GSI1SK": "REG#event456",
    "userId": "user123",
    "eventId": "event456",
    "status": "registered",
    "position": 0,
    "registeredAt": "2024-01-01T10:00:00Z"
}

# Registration Item (waitlisted)
{
    "PK": "EVENT#event456",
    "SK": "REG#waitlisted#0001#user789",
    "GSI1PK": "USER#user789",
    "GSI1SK": "REG#event456",
    "userId": "user789",
    "eventId": "event456",
    "status": "waitlisted",
    "position": 1,
    "registeredAt": "2024-01-01T11:00:00Z"
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: User creation round trip
*For any* valid userId and name, creating a user and then retrieving it should return a user with the same userId and name.
**Validates: Requirements 1.1**

### Property 2: Event initialization invariant
*For any* newly created event, the registeredCount field should be initialized to zero.
**Validates: Requirements 2.4**

### Property 3: Waitlist ordering preservation
*For any* event with a waitlist, users should be added to the waitlist in chronological order, and this order should be maintained through all operations.
**Validates: Requirements 3.3, 6.2**

### Property 4: Registration count consistency
*For any* event at any point in time, the registeredCount field should exactly match the number of users with status "registered" for that event.
**Validates: Requirements 6.1**

### Property 5: Waitlist promotion on unregister
*For any* event with available capacity and a non-empty waitlist, when a registered user unregisters, the first user in the waitlist should be promoted to registered status.
**Validates: Requirements 4.2**

### Property 6: Waitlist removal preserves order
*For any* user in a waitlist at position N, removing that user should not change the relative order of users at positions before or after N.
**Validates: Requirements 4.3**

### Property 7: User registrations query accuracy
*For any* user, querying their registered events should return exactly the set of events where they have status "registered" and should exclude events where they have status "waitlisted".
**Validates: Requirements 5.1, 5.2**

### Property 8: Registration increases count by one
*For any* event with available capacity and any user not already registered, successfully registering the user should increase the registeredCount by exactly 1.
**Validates: Requirements 3.1**

### Property 9: Unregistration decreases count by one
*For any* registered user and event, successfully unregistering the user should decrease the registeredCount by exactly 1 (unless a waitlisted user is promoted, in which case count remains the same).
**Validates: Requirements 4.1**

## Error Handling

### Validation Errors (HTTP 422)
- Missing required fields (userId, name, eventId)
- Invalid capacity values (≤ 0)
- Duplicate userId on user creation
- Duplicate registration attempts
- Invalid event or user IDs

### Not Found Errors (HTTP 404)
- Event does not exist
- User does not exist
- Registration does not exist

### Business Logic Errors (HTTP 409)
- Event at capacity without waitlist
- Cannot unregister when not registered

### Error Response Format
```json
{
    "detail": "Error message describing the issue"
}
```

### Transaction Handling
- Use DynamoDB transactions for operations that modify multiple items
- Registration operations that update both registration and event count must be atomic
- Waitlist promotion must atomically remove from waitlist and add to registered
- On transaction failure, return appropriate error without partial state changes

## Testing Strategy

### Unit Testing
We'll use pytest for unit testing with the following focus areas:

**Model Validation Tests:**
- Test User model creation with valid and invalid data
- Test Event model with various capacity and waitlist configurations
- Test Registration model with different statuses

**Business Logic Tests:**
- Test RegistrationManager with specific scenarios
- Test WaitlistManager promotion logic
- Test edge cases like empty waitlists, full events

**API Endpoint Tests:**
- Test each endpoint with valid requests
- Test error responses for invalid inputs
- Test authentication and authorization (if implemented)

### Property-Based Testing
We'll use Hypothesis (Python property-based testing library) to verify universal properties:

**Configuration:**
- Each property-based test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate random but valid test data
- Each test will be tagged with a comment referencing the design document property

**Test Tagging Format:**
```python
# Feature: user-registration, Property 1: User creation round trip
@given(user_id=text(), name=text())
def test_user_creation_round_trip(user_id, name):
    ...
```

**Property Test Coverage:**
1. **Property 1** - User creation round trip: Generate random users, create them, retrieve them, verify data matches
2. **Property 2** - Event initialization: Generate random events, verify registeredCount starts at 0
3. **Property 3** - Waitlist ordering: Generate random registration sequences, verify chronological order maintained
4. **Property 4** - Count consistency: Perform random registration/unregistration operations, verify count always matches actual registrations
5. **Property 5** - Waitlist promotion: Generate events with waitlists, unregister users, verify first waitlisted user promoted
6. **Property 6** - Waitlist order preservation: Remove random users from waitlist, verify remaining order unchanged
7. **Property 7** - Query accuracy: Generate random registrations and waitlist entries, verify query returns only registered events
8. **Property 8** - Registration increment: Generate random valid registrations, verify count increases by 1
9. **Property 9** - Unregistration decrement: Generate random unregistrations, verify count decreases appropriately

**Hypothesis Strategies:**
- `user_ids`: Valid string identifiers
- `names`: Non-empty strings
- `event_ids`: Valid event identifiers
- `capacities`: Positive integers (1-1000)
- `registration_sequences`: Lists of (user_id, event_id) tuples

### Integration Testing
- Test complete registration flows end-to-end
- Test DynamoDB transaction behavior
- Test concurrent registration scenarios (if time permits)

### Test Data Management
- Use DynamoDB Local for testing
- Create test fixtures for common scenarios
- Clean up test data after each test run
