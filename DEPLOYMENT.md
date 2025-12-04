# Events API Deployment Guide

## Quick Deploy

Deploy the complete serverless Events API to AWS:

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy
```

The deployment will output your API endpoint URL.

## What Gets Deployed

1. **DynamoDB Table** - Stores event data with pay-per-request billing
2. **Lambda Function** - Runs FastAPI application (Python 3.11)
3. **API Gateway** - Public REST API endpoint with CORS enabled

## Testing the API

Once deployed, test with the endpoint URL from CDK outputs:

```bash
# Set your API endpoint
export API_URL="https://your-api-id.execute-api.us-east-1.amazonaws.com/prod"

# Create an event
curl -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "api-test-event-456",
    "title": "API Gateway Test Event",
    "description": "Testing API Gateway integration",
    "date": "2024-12-15",
    "location": "API Test Location",
    "capacity": 200,
    "organizer": "API Test Organizer",
    "status": "active"
  }'

# List all events
curl "$API_URL/events"

# List events by status
curl "$API_URL/events?status=active"

# Get specific event
curl "$API_URL/events/api-test-event-456"

# Update event
curl -X PUT "$API_URL/events/api-test-event-456" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated API Gateway Test Event",
    "capacity": 250
  }'

# Delete event
curl -X DELETE "$API_URL/events/api-test-event-456"
```

## API Endpoints

All endpoints support the required test cases:

- `GET /events` - List all events (200)
- `GET /events?status=active` - Filter by status (200)
- `POST /events` - Create event, returns eventId (201)
- `GET /events/{eventId}` - Get specific event (200)
- `PUT /events/{eventId}` - Update event (200)
- `DELETE /events/{eventId}` - Delete event (200)

## Event Schema

```json
{
  "eventId": "string (optional on create, auto-generated if not provided)",
  "title": "string (required)",
  "description": "string (required)",
  "date": "string (required, YYYY-MM-DD format)",
  "location": "string (required)",
  "capacity": "integer (required, > 0)",
  "organizer": "string (required)",
  "status": "string (required: draft|published|cancelled|completed|active)",
  "createdAt": "string (auto-generated)",
  "updatedAt": "string (auto-generated)"
}
```

## CORS Configuration

CORS is enabled for all origins, methods, and standard headers to support web applications.

## Cost Optimization

- **DynamoDB**: Pay-per-request billing (no idle costs)
- **Lambda**: Pay only for execution time
- **API Gateway**: Pay per request
- **Estimated cost**: ~$0.50-2.00/month for light usage

## Cleanup

Remove all resources:

```bash
cd infrastructure
cdk destroy
```

## Troubleshooting

### Check Lambda logs
```bash
aws logs tail /aws/lambda/EventsAPIStack-EventsAPIFunction --follow
```

### Test Lambda directly
```bash
aws lambda invoke --function-name EventsAPIStack-EventsAPIFunction \
  --payload '{"httpMethod":"GET","path":"/events"}' response.json
cat response.json
```

### Verify DynamoDB table
```bash
aws dynamodb describe-table --table-name EventsAPIStack-EventsTable
```
