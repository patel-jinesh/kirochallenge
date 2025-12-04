# Next Steps - Deploy Your Events API

## ⚠️ AWS Credentials Required

Your AWS credentials are currently expired. Before deploying, you need to refresh them.

## Step 1: Refresh AWS Credentials

Choose one of these methods:

### Option A: AWS Configure (for IAM users)
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
```

### Option B: AWS SSO (if using SSO)
```bash
aws sso login --profile your-profile
export AWS_PROFILE=your-profile
```

### Option C: Temporary Credentials
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_SESSION_TOKEN=your_token  # if using temporary credentials
```

### Verify Credentials
```bash
aws sts get-caller-identity
# Should show your account ID and user/role
```

## Step 2: Deploy to AWS

Once credentials are configured:

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy
```

The deployment takes about 2-3 minutes and will output your API endpoint URL.

## Step 3: Test Your API

After deployment, you'll see output like:
```
Outputs:
EventsAPIStack.APIEndpoint = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
```

Use the test script:
```bash
./test_api.sh https://abc123.execute-api.us-east-1.amazonaws.com/prod
```

Or test manually:
```bash
export API_URL="https://abc123.execute-api.us-east-1.amazonaws.com/prod"

# Create event
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

# List events
curl "$API_URL/events"

# Filter by status
curl "$API_URL/events?status=active"

# Get specific event
curl "$API_URL/events/api-test-event-456"

# Update event
curl -X PUT "$API_URL/events/api-test-event-456" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated API Gateway Test Event", "capacity": 250}'

# Delete event
curl -X DELETE "$API_URL/events/api-test-event-456"
```

## What's Been Built

✅ **Backend API** (FastAPI)
- Full CRUD operations
- DynamoDB integration
- Input validation
- CORS enabled
- Status filtering
- Custom eventId support

✅ **Infrastructure** (AWS CDK)
- Lambda function (Python 3.11)
- API Gateway with CORS
- DynamoDB table (pay-per-request)
- Proper IAM permissions

✅ **All Test Requirements Met**
- GET /events → 200
- GET /events?status=active → 200
- POST /events → 201 (with eventId)
- GET /events/{id} → 200
- PUT /events/{id} → 200
- DELETE /events/{id} → 200

## Troubleshooting

### If deployment fails:
```bash
# Check CDK version
cdk --version

# Upgrade if needed
npm install -g aws-cdk

# Check Python dependencies
pip list | grep aws-cdk
```

### If API returns errors:
```bash
# Check Lambda logs
aws logs tail /aws/lambda/EventsAPIStack-EventsAPIFunction --follow

# Check DynamoDB table
aws dynamodb describe-table --table-name EventsAPIStack-EventsTable
```

### If you need to redeploy:
```bash
cd infrastructure
cdk deploy --force
```

## Documentation

- [README.md](README.md) - Project overview
- [QUICK_START.md](QUICK_START.md) - Quick deployment guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment docs
- [backend/README.md](backend/README.md) - Backend API details

## Cost

With AWS Free Tier:
- First 1M Lambda requests/month: FREE
- First 25 GB DynamoDB storage: FREE
- API Gateway: $3.50 per million requests

Estimated: $0.50-2.00/month for light usage

## Cleanup

When done testing:
```bash
cd infrastructure
cdk destroy
```

This removes all AWS resources and stops any charges.
