---
inclusion: fileMatch
fileMatchPattern: '**/*{api,handler,main,route}*.{py,js,ts}'
---

# REST API Standards

## HTTP Methods
- GET: Retrieve resources
- POST: Create new resources
- PUT: Update/replace entire resources
- PATCH: Partial resource updates
- DELETE: Remove resources

## Status Codes
- 200 OK: Successful request
- 201 Created: Successful resource creation
- 400 Bad Request: Invalid request
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server error

## Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## JSON Response Format Standards
- Use consistent JSON structure for all responses
- Include appropriate status codes
- Return proper Content-Type: application/json headers
