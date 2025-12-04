#!/bin/bash

# Events API Test Script
# Usage: ./test_api.sh <API_URL>

if [ -z "$1" ]; then
    echo "Usage: ./test_api.sh <API_URL>"
    echo "Example: ./test_api.sh https://xxxxx.execute-api.us-east-1.amazonaws.com/prod"
    exit 1
fi

API_URL="$1"
EVENT_ID="api-test-event-456"

echo "Testing Events API at: $API_URL"
echo "========================================"
echo ""

# Test 1: Create Event
echo "Test 1: POST /events (Create Event)"
echo "Expected: 201 Created"
curl -s -w "\nHTTP Status: %{http_code}\n" -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "'"$EVENT_ID"'",
    "title": "API Gateway Test Event",
    "description": "Testing API Gateway integration",
    "date": "2024-12-15",
    "location": "API Test Location",
    "capacity": 200,
    "organizer": "API Test Organizer",
    "status": "active"
  }'
echo ""
echo "========================================"
echo ""

# Test 2: List All Events
echo "Test 2: GET /events (List All Events)"
echo "Expected: 200 OK"
curl -s -w "\nHTTP Status: %{http_code}\n" "$API_URL/events"
echo ""
echo "========================================"
echo ""

# Test 3: Filter by Status
echo "Test 3: GET /events?status=active (Filter by Status)"
echo "Expected: 200 OK"
curl -s -w "\nHTTP Status: %{http_code}\n" "$API_URL/events?status=active"
echo ""
echo "========================================"
echo ""

# Test 4: Get Specific Event
echo "Test 4: GET /events/$EVENT_ID (Get Specific Event)"
echo "Expected: 200 OK"
curl -s -w "\nHTTP Status: %{http_code}\n" "$API_URL/events/$EVENT_ID"
echo ""
echo "========================================"
echo ""

# Test 5: Update Event
echo "Test 5: PUT /events/$EVENT_ID (Update Event)"
echo "Expected: 200 OK"
curl -s -w "\nHTTP Status: %{http_code}\n" -X PUT "$API_URL/events/$EVENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated API Gateway Test Event",
    "capacity": 250
  }'
echo ""
echo "========================================"
echo ""

# Test 6: Delete Event
echo "Test 6: DELETE /events/$EVENT_ID (Delete Event)"
echo "Expected: 200 OK"
curl -s -w "\nHTTP Status: %{http_code}\n" -X DELETE "$API_URL/events/$EVENT_ID"
echo ""
echo "========================================"
echo ""

echo "All tests completed!"
echo ""
echo "Summary of Expected Status Codes:"
echo "  POST /events              -> 201"
echo "  GET /events               -> 200"
echo "  GET /events?status=active -> 200"
echo "  GET /events/{id}          -> 200"
echo "  PUT /events/{id}          -> 200"
echo "  DELETE /events/{id}       -> 200"
