# Events API - Quick Start Guide

## ✅ What's Ready

Your FastAPI Events API is fully configured and ready to deploy with:

- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ DynamoDB integration
- ✅ Input validation with Pydantic
- ✅ CORS enabled for web access
- ✅ Status filtering support (`?status=active`)
- ✅ Custom eventId support for testing
- ✅ Proper error handling
- ✅ Lambda + API Gateway deployment via CDK
- ✅ All test endpoint requirements met

## 🚀 Deploy to AWS

### Step 1: Configure AWS Credentials

```bash
aws configure
# Or refresh your AWS SSO session if using SSO
aws sso login --profile your-profile
```

### Step 2: Deploy

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy
```

### Step 3: Get Your API URL

After deployment completes, CDK will output:
```
Outputs:
EventsAPIStack.APIEndpoint = https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/
```

## 🧪 Test Your API

Replace `YOUR_API_URL` with your actual endpoint:

```bash
export API_URL="https://xxxxx.execute-api.us-east-1.amazonaws.com/prod"

# Test 1: Create event (201)
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

# Test 2: List all events (200)
curl "$API_URL/events"

# Test 3: Filter by status (200)
curl "$API_URL/events?status=active"

# Test 4: Get specific event (200)
curl "$API_URL/events/api-test-event-456"

# Test 5: Update event (200)
curl -X PUT "$API_URL/events/api-test-event-456" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated API Gateway Test Event",
    "capacity": 250
  }'

# Test 6: Delete event (200)
curl -X DELETE "$API_URL/events/api-test-event-456"
```

## 📋 Test Requirements Met

All required test endpoints are implemented:

| Endpoint | Method | Status | Features |
|----------|--------|--------|----------|
| `/events` | GET | 200 | List all events |
| `/events?status=active` | GET | 200 | Filter by status |
| `/events` | POST | 201 | Create with eventId |
| `/events/{id}` | GET | 200 | Get specific event |
| `/events/{id}` | PUT | 200 | Update event |
| `/events/{id}` | DELETE | 200 | Delete event |

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI app with all endpoints
├── models.py            # Pydantic models with validation
├── database.py          # DynamoDB client
├── lambda_handler.py    # Lambda entry point
└── requirements.txt     # Dependencies

infrastructure/
├── app.py              # CDK app
├── stacks/
│   └── backend_stack.py # Lambda + API Gateway + DynamoDB
└── requirements.txt    # CDK dependencies
```

## 🔧 Local Development (Optional)

To run locally with DynamoDB Local:

```bash
# Start DynamoDB Local (Docker)
docker run -p 8000:8000 amazon/dynamodb-local

# Set environment
export AWS_ENDPOINT_URL=http://localhost:8000
export DYNAMODB_TABLE_NAME=EventsTable
export AWS_REGION=us-east-1

# Create table
aws dynamodb create-table \
  --table-name EventsTable \
  --attribute-definitions AttributeName=eventId,AttributeType=S \
  --key-schema AttributeName=eventId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000

# Run API
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 💰 Cost Estimate

- DynamoDB: Pay-per-request (~$1.25 per million writes)
- Lambda: First 1M requests free, then $0.20 per 1M
- API Gateway: $3.50 per million requests
- **Estimated**: $0.50-2.00/month for light usage

## 🧹 Cleanup

```bash
cd infrastructure
cdk destroy
```

## 📚 Documentation

- API Docs: `{API_URL}/docs` (Swagger UI)
- ReDoc: `{API_URL}/redoc`
- See `DEPLOYMENT.md` for detailed deployment guide
- See `backend/README.md` for backend details
