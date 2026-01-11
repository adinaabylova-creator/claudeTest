# UIGen API Documentation

## Overview

UIGen provides a RESTful API for AI-powered React component generation. The API is built on Next.js API Routes and uses TypeScript for type safety.

**Base URL**: `http://localhost:3000/api` (development)

**Authentication**: Session-based authentication using HTTP-only cookies

**Content Type**: `application/json`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Component Generation](#component-generation)
3. [Component Management](#component-management)
4. [Chat/Conversation](#chatconversation)
5. [Export](#export)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)

---

## Authentication

### POST /api/auth/signup

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "createdAt": "2026-01-11T10:30:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid email or weak password
- `409 Conflict` - Email already registered

---

### POST /api/auth/login

Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "email": "user@example.com"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing required fields

---

### POST /api/auth/logout

End the current user session.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### POST /api/auth/anonymous

Create an anonymous session for users who don't want to register.

**Response (200 OK):**
```json
{
  "success": true,
  "sessionId": "anon_xyz789",
  "expiresAt": "2026-01-11T22:30:00Z"
}
```

**Notes:**
- Anonymous sessions expire after 12 hours of inactivity
- Components created in anonymous sessions are not persisted

---

### GET /api/auth/session

Get current session information.

**Response (200 OK):**
```json
{
  "authenticated": true,
  "user": {
    "id": "user_123",
    "email": "user@example.com"
  }
}
```

**Response (401 Unauthorized) - Not authenticated:**
```json
{
  "authenticated": false
}
```

---

## Component Generation

### POST /api/generate

Generate a React component based on a text description using Claude AI.

**Request Body:**
```json
{
  "prompt": "Create a login form with email and password fields, and a submit button",
  "conversationId": "conv_123",
  "previousCode": null
}
```

**Parameters:**
- `prompt` (required): Natural language description of the component
- `conversationId` (optional): ID to continue a previous conversation
- `previousCode` (optional): Existing code to refine/modify

**Response (200 OK):**
```json
{
  "success": true,
  "component": {
    "id": "comp_456",
    "name": "LoginForm",
    "files": [
      {
        "path": "LoginForm.tsx",
        "content": "import React, { useState } from 'react';\n\nexport default function LoginForm() {\n  const [email, setEmail] = useState('');\n  const [password, setPassword] = useState('');\n  \n  return (\n    <form className=\"max-w-md mx-auto\">\n      <input type=\"email\" value={email} onChange={(e) => setEmail(e.target.value)} />\n      <input type=\"password\" value={password} onChange={(e) => setPassword(e.target.value)} />\n      <button type=\"submit\">Submit</button>\n    </form>\n  );\n}"
      }
    ],
    "conversationId": "conv_123",
    "timestamp": "2026-01-11T10:30:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid prompt
- `429 Too Many Requests` - Rate limit exceeded
- `503 Service Unavailable` - AI service temporarily unavailable

**Notes:**
- Without an Anthropic API key, returns static placeholder code
- Responses may take 5-30 seconds depending on complexity
- Maximum prompt length: 2000 characters

---

## Component Management

### GET /api/components

Retrieve all components for the authenticated user.

**Query Parameters:**
- `limit` (optional): Number of components to return (default: 20, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `sortBy` (optional): Sort field - `createdAt` or `updatedAt` (default: `createdAt`)
- `order` (optional): `asc` or `desc` (default: `desc`)

**Response (200 OK):**
```json
{
  "success": true,
  "components": [
    {
      "id": "comp_123",
      "name": "LoginForm",
      "description": "A login form with validation",
      "createdAt": "2026-01-10T15:20:00Z",
      "updatedAt": "2026-01-11T09:15:00Z",
      "fileCount": 2
    },
    {
      "id": "comp_456",
      "name": "UserCard",
      "description": "A card component displaying user information",
      "createdAt": "2026-01-09T12:00:00Z",
      "updatedAt": "2026-01-09T12:00:00Z",
      "fileCount": 1
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `400 Bad Request` - Invalid query parameters

---

### GET /api/components/:id

Retrieve a specific component by ID.

**Response (200 OK):**
```json
{
  "success": true,
  "component": {
    "id": "comp_123",
    "name": "LoginForm",
    "description": "A login form with validation",
    "files": [
      {
        "path": "LoginForm.tsx",
        "content": "import React from 'react';\n\n// Component code here..."
      },
      {
        "path": "LoginForm.test.tsx",
        "content": "import { render } from '@testing-library/react';\n\n// Test code here..."
      }
    ],
    "createdAt": "2026-01-10T15:20:00Z",
    "updatedAt": "2026-01-11T09:15:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `404 Not Found` - Component not found or access denied

---

### POST /api/components

Save a generated component to the user's library.

**Request Body:**
```json
{
  "name": "LoginForm",
  "description": "A login form with email and password fields",
  "files": [
    {
      "path": "LoginForm.tsx",
      "content": "import React from 'react';\n\nexport default function LoginForm() { ... }"
    }
  ],
  "conversationId": "conv_123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "component": {
    "id": "comp_789",
    "name": "LoginForm",
    "description": "A login form with email and password fields",
    "createdAt": "2026-01-11T10:30:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated (anonymous users cannot save)
- `400 Bad Request` - Invalid component data
- `413 Payload Too Large` - Component exceeds size limit (5MB)

---

### PUT /api/components/:id

Update an existing component.

**Request Body:**
```json
{
  "name": "ImprovedLoginForm",
  "description": "Updated description",
  "files": [
    {
      "path": "LoginForm.tsx",
      "content": "// Updated code..."
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "component": {
    "id": "comp_123",
    "name": "ImprovedLoginForm",
    "updatedAt": "2026-01-11T11:00:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `404 Not Found` - Component not found
- `403 Forbidden` - User doesn't own this component

---

### DELETE /api/components/:id

Delete a component from the user's library.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Component deleted successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `404 Not Found` - Component not found
- `403 Forbidden` - User doesn't own this component

---

## Chat/Conversation

### POST /api/chat

Send a message to refine or iterate on a component using conversational AI.

**Request Body:**
```json
{
  "message": "Add form validation and error messages",
  "conversationId": "conv_123",
  "currentCode": {
    "files": [
      {
        "path": "LoginForm.tsx",
        "content": "// Current component code..."
      }
    ]
  }
}
```

**Response (200 OK - Streaming):**

This endpoint returns a Server-Sent Events (SSE) stream:

```
data: {"type":"message","content":"I'll add form validation"}

data: {"type":"code","file":"LoginForm.tsx","content":"import React, { useState } from 'react';"}

data: {"type":"code","file":"LoginForm.tsx","content":"\n\nexport default function LoginForm() {"}

data: {"type":"complete","conversationId":"conv_123"}
```

**Event Types:**
- `message` - AI assistant message text
- `code` - Generated code chunks
- `error` - Error occurred during generation
- `complete` - Generation finished

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `400 Bad Request` - Missing required fields
- `429 Too Many Requests` - Rate limit exceeded

**Notes:**
- Responses are streamed in real-time
- Client should use EventSource or similar for consuming SSE
- Conversation history is maintained server-side

---

## Export

### POST /api/export

Export generated component code in various formats.

**Request Body:**
```json
{
  "componentId": "comp_123",
  "format": "zip"
}
```

**Parameters:**
- `componentId` (required): ID of the component to export
- `format` (required): Export format - `zip`, `json`, or `files`

**Response (200 OK) - For `zip` format:**

Binary response with `Content-Type: application/zip`

**Response (200 OK) - For `json` format:**
```json
{
  "success": true,
  "component": {
    "name": "LoginForm",
    "files": [
      {
        "path": "LoginForm.tsx",
        "content": "// Component code..."
      }
    ]
  }
}
```

**Response (200 OK) - For `files` format:**
```json
{
  "success": true,
  "files": {
    "LoginForm.tsx": "// Component code...",
    "LoginForm.test.tsx": "// Test code..."
  }
}
```

**Error Responses:**
- `401 Unauthorized` - User not authenticated
- `404 Not Found` - Component not found
- `400 Bad Request` - Invalid format specified

---

## Error Handling

All API errors follow a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` - Request validation failed
- `AUTHENTICATION_REQUIRED` - User must be authenticated
- `AUTHORIZATION_FAILED` - User lacks permission
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `AI_SERVICE_ERROR` - Claude AI service error
- `INTERNAL_ERROR` - Unexpected server error

---

## Rate Limiting

API endpoints are rate-limited to ensure fair usage:

**Anonymous Users:**
- 10 requests per minute per IP
- 100 requests per hour per IP

**Authenticated Users:**
- 30 requests per minute per user
- 500 requests per hour per user

**Rate Limit Headers:**

All responses include rate limit information:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 27
X-RateLimit-Reset: 1704971400
```

**Rate Limit Exceeded Response (429):**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests, please try again later",
    "retryAfter": 45
  }
}
```

---

## WebSocket API (Optional)

For real-time preview updates, UIGen supports WebSocket connections:

**Connection URL:** `ws://localhost:3000/api/ws`

**Authentication:** Send session token in first message

**Message Format:**
```json
{
  "type": "subscribe",
  "componentId": "comp_123"
}
```

**Server Events:**
```json
{
  "type": "codeUpdate",
  "componentId": "comp_123",
  "file": "LoginForm.tsx",
  "content": "// Updated code..."
}
```

---

## SDK Examples

### JavaScript/TypeScript

```typescript
// Using fetch API
async function generateComponent(prompt: string) {
  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}

// Using EventSource for streaming
function streamChat(message: string, conversationId: string) {
  const eventSource = new EventSource(
    `/api/chat?message=${encodeURIComponent(message)}&conversationId=${conversationId}`
  );

  eventSource.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
  });

  eventSource.addEventListener('error', (error) => {
    console.error('Stream error:', error);
    eventSource.close();
  });

  return eventSource;
}
```

### Python

```python
import requests

class UIGenClient:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, email: str, password: str):
        response = self.session.post(
            f"{self.base_url}/api/auth/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    def generate_component(self, prompt: str):
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()

    def get_components(self, limit=20):
        response = self.session.get(
            f"{self.base_url}/api/components",
            params={"limit": limit}
        )
        response.raise_for_status()
        return response.json()
```

---

## Changelog

### Version 1.0.0 (2026-01-11)
- Initial API release
- Basic authentication endpoints
- Component generation with Claude AI
- Component management CRUD operations
- Chat/conversation support
- Export functionality

---

## Support

For issues, questions, or feature requests, please visit:
- GitHub Issues: [https://github.com/your-repo/uigen/issues](https://github.com/your-repo/uigen/issues)
- Documentation: [https://uigen.dev/docs](https://uigen.dev/docs)

---

## License

This API is part of the UIGen project and is subject to the project's license terms.
