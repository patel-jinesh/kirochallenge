---
inclusion: always
---

# AWS Credentials Management

## Terminal Session Awareness
When running AWS CLI commands or CDK operations:
- Check if AWS credentials are available in the current environment
- If a command fails due to missing credentials, prompt the user to provide them
- Avoid creating new terminal sessions unnecessarily as they lose environment variables
- Reuse existing terminal sessions when possible

## Credential Prompts
Before running AWS operations (deploy, cdk commands, aws cli), remind the user:
"Make sure your AWS credentials are configured. If needed, run:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=your_region
```
Or use `aws configure` for persistent configuration."

## Best Practices
- Never hardcode credentials in code
- Use environment variables or AWS credential files
- Prefer IAM roles when running on AWS infrastructure
- Keep credentials out of version control
