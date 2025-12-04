---
inclusion: fileMatch
fileMatchPattern: '**/*{api,handler,main,route}*.{py,js,ts}'
---

# REST API Standards

## HTTP Methods
- GET: Retrieve resources (idempotent, no body)
- POST: Create new resources
- PUT: Update/replace entire resources
- PATCH: Partial resource updates
- DELETE: Remove resources

## Status Codes
- 200 OK: Successful GET, PUT, PATCH, DELETE
- 201 Created: Successful POST with resource creation
- 204 No Content: Successful DELETE with no response body
- 400 Bad Request: Invalid request data or parameters
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Authenticated but insufficient permissions
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Resource conflict (e.g., duplicate)
- 422 Unprocessable Entity: Validation errors
- 500 Internal Server Error: Server-side errors

## Error Response Format
All error responses must follow this structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}  // Optional: additional context
  }
}
```

## Success Response Format
All successful responses should follow:
```json
{
  "data": {},  // The actual response data
  "meta": {    // Optional: pagination, timestamps, etc.
    "timestamp": "ISO-8601 datetime",
    "count": 0
  }
}
```

## General Conventions
- Use plural nouns for endpoints: `/users`, `/items`
- Use kebab-case for multi-word resources: `/user-profiles`
- Version APIs in URL: `/api/v1/resource`
- Use query parameters for filtering, sorting, pagination
- Return appropriate Content-Type headers (application/json)
- Include CORS headers when needed
- Use consistent field naming (snake_case or camelCase, not mixed)
