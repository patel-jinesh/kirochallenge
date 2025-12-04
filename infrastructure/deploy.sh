#!/bin/bash

# Deploy script for Events API

set -e

echo "Installing CDK dependencies..."
pip install -r requirements.txt

echo "Bootstrapping CDK (if needed)..."
cdk bootstrap

echo "Deploying stack..."
cdk deploy --require-approval never

echo "Deployment complete!"
echo "Check the outputs above for your API endpoint URL"
