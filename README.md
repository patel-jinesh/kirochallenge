# Events API

A production-ready serverless REST API for managing events, built with FastAPI, AWS Lambda, API Gateway, and DynamoDB. Features automatic scaling, pay-per-request pricing, and comprehensive API documentation.

## 🌐 Live API

**Base URL:** `https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod`

**Interactive Documentation:**
- Swagger UI: https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod/docs
- ReDoc: https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod/redoc
- Code Documentation: [backend/docs/](backend/docs/)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- AWS Account with configured credentials
- AWS CDK CLI (`npm install -g aws-cdk`)
- Node.js 14+ (for CDK)

### Using the Deployed API

```bash
# Set API URL
export API_URL="https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod"

# Create an event
curl -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-12-15",
    "location": "San Francisco, CA",
    "capacity": 500,
    "organizer": "Tech Events Inc",
    "status": "active"
  }'

# List all events
curl "$API_URL/events"

# Get specific event
curl "$API_URL/events/{eventId}"

# Filter by status
curl "$API_URL/events?status=active"

# Update an event
curl -X PUT "$API_URL/events/{eventId}" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete an event
curl -X DELETE "$API_URL/events/{eventId}"
```

### Deploy Your Own

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd events-api

# 2. Configure AWS credentials
aws configure

# 3. Install dependencies
cd infrastructure
pip install -r requirements.txt

# 4. Bootstrap CDK (first time only)
cdk bootstrap

# 5. Deploy to AWS
cdk deploy

# 6. Test your deployment
./test_api.sh <your-api-url>
```

**See [QUICK_START.md](QUICK_START.md) for complete deployment and testing guide.**

## ✨ Features

- ✅ **Full CRUD Operations** - Create, read, update, and delete events
- ✅ **Serverless Architecture** - AWS Lambda + API Gateway for automatic scaling
- ✅ **NoSQL Database** - DynamoDB with pay-per-request billing
- ✅ **CORS Enabled** - Ready for web application integration
- ✅ **Data Validation** - Pydantic models with comprehensive validation
- ✅ **Auto-generated Fields** - Automatic timestamps and unique IDs
- ✅ **Status Filtering** - Query events by status (draft, published, active, etc.)
- ✅ **OpenAPI Documentation** - Interactive Swagger UI and ReDoc
- ✅ **Infrastructure as Code** - AWS CDK for reproducible deployments
- ✅ **Cost-Effective** - ~$0.50-2.00/month with AWS Free Tier

## 📡 API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check | 200 |
| POST | `/events` | Create a new event | 201 |
| GET | `/events` | List all events | 200 |
| GET | `/events?status={status}` | Filter events by status | 200 |
| GET | `/events/{eventId}` | Get specific event | 200 |
| PUT | `/events/{eventId}` | Update an event | 200 |
| DELETE | `/events/{eventId}` | Delete an event | 200 |

## 📋 Event Schema

### Request Body (Create/Update)

```json
{
  "title": "string (1-200 chars, required)",
  "description": "string (max 1000 chars, required)",
  "date": "YYYY-MM-DD (ISO format, required)",
  "location": "string (1-200 chars, required)",
  "capacity": "integer > 0 (required)",
  "organizer": "string (1-100 chars, required)",
  "status": "draft|published|cancelled|completed|active (required)"
}
```

### Response Body

```json
{
  "eventId": "string (UUID, auto-generated)",
  "title": "string",
  "description": "string",
  "date": "YYYY-MM-DD",
  "location": "string",
  "capacity": "integer",
  "organizer": "string",
  "status": "string",
  "createdAt": "ISO timestamp",
  "updatedAt": "ISO timestamp"
}
```

### Status Values

- `draft` - Event is being planned
- `published` - Event is publicly visible
- `active` - Event is currently happening
- `completed` - Event has finished
- `cancelled` - Event was cancelled

## Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # API endpoints
│   ├── models.py        # Pydantic models
│   ├── database.py      # DynamoDB client
│   └── lambda_handler.py # Lambda entry point
├── infrastructure/       # AWS CDK
│   ├── app.py           # CDK app
│   └── stacks/          # Stack definitions
├── QUICK_START.md       # Deployment guide
└── DEPLOYMENT.md        # Detailed deployment docs
```

## 📚 Documentation

### API Documentation
- [Swagger UI](https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod/docs) - Interactive API testing
- [ReDoc](https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod/redoc) - API reference
- [Code Documentation](backend/docs/) - Python module documentation (pdoc)

### Deployment Guides
- [QUICK_START.md](QUICK_START.md) - Fast deployment and testing
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md) - Current deployment details

### Component Documentation
- [backend/README.md](backend/README.md) - Backend API details
- [infrastructure/README.md](infrastructure/README.md) - Infrastructure details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)

## 🧪 Testing

### Automated Test Suite

Run the comprehensive test script:

```bash
./test_api.sh https://o1anr7n0je.execute-api.us-east-1.amazonaws.com/prod
```

The test suite validates:
- Health check endpoint
- Event creation
- Event retrieval
- Event listing
- Status filtering
- Event updates
- Event deletion

### Manual Testing

Use the interactive Swagger UI at `/docs` endpoint for manual testing and exploration.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│   Client    │─────▶│ API Gateway  │─────▶│   Lambda    │─────▶│  DynamoDB    │
│ (Browser/   │      │   (REST)     │      │  (FastAPI)  │      │  (NoSQL DB)  │
│  CLI/App)   │◀─────│              │◀─────│             │◀─────│              │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
```

### Components

- **API Gateway**: HTTP API with CORS support
- **Lambda Function**: Python 3.9 runtime with FastAPI + Mangum
- **DynamoDB**: NoSQL database with on-demand billing
- **AWS CDK**: Infrastructure as Code for deployment

## 💰 Cost Estimation

With AWS Free Tier:
- **Lambda**: 1M requests/month free, then $0.20 per 1M requests
- **API Gateway**: 1M requests/month free, then $1.00 per 1M requests
- **DynamoDB**: 25GB storage free, 25 WCU/RCU free

**Estimated monthly cost**: $0.50-2.00 for light usage (within free tier)

## 🧹 Cleanup

To remove all deployed resources and avoid charges:

```bash
cd infrastructure
cdk destroy
```

This will delete:
- API Gateway
- Lambda function
- DynamoDB table (and all data)
- IAM roles and policies

## 💻 Local Development

### Running Locally

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 3. Run with uvicorn
uvicorn main:app --reload --port 8000

# 4. Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Using DynamoDB Local

```bash
# 1. Start DynamoDB Local (Docker)
docker run -p 8000:8000 amazon/dynamodb-local

# 2. Set environment variable
export AWS_ENDPOINT_URL=http://localhost:8000

# 3. Create table
aws dynamodb create-table \
  --table-name EventsTable \
  --attribute-definitions AttributeName=eventId,AttributeType=S \
  --key-schema AttributeName=eventId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000
```

See [backend/README.md](backend/README.md) for more details.
