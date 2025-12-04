# Infrastructure

CDK infrastructure for deploying the Events API as a serverless application.

## Architecture

- **API Gateway**: REST API endpoint with CORS enabled
- **Lambda**: Python 3.11 function running FastAPI with Mangum
- **DynamoDB**: NoSQL database for event storage (pay-per-request billing)

## Prerequisites

- AWS CLI configured with credentials
- Python 3.11+
- Node.js (for CDK CLI)
- AWS CDK CLI: `npm install -g aws-cdk`

## Deploy

1. Install dependencies:
```bash
cd infrastructure
pip install -r requirements.txt
```

2. Bootstrap CDK (first time only):
```bash
cdk bootstrap
```

3. Deploy the stack:
```bash
cdk deploy
```

Or use the deploy script:
```bash
chmod +x deploy.sh
./deploy.sh
```

4. Note the API endpoint URL from the outputs

## Useful Commands

- `cdk diff` - Compare deployed stack with current state
- `cdk synth` - Synthesize CloudFormation template
- `cdk destroy` - Remove all resources

## Outputs

After deployment, you'll receive:
- **APIEndpoint**: Your public API URL
- **DynamoDBTableName**: The DynamoDB table name
- **LambdaFunctionName**: The Lambda function name
