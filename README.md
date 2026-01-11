# UIGen

AI-powered React component generator with live preview.

## Prerequisites

- Node.js 18+
- npm

## Setup

1. **Optional** Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

The project will run without an API key. Rather than using a LLM to generate components, static code will be returned instead.

2. Install dependencies and initialize database

```bash
npm run setup
```

This command will:

- Install all dependencies
- Generate Prisma client
- Run database migrations

## Running the Application

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Usage

1. Sign up or continue as anonymous user
2. Describe the React component you want to create in the chat
3. View generated components in real-time preview
4. Switch to Code view to see and edit the generated files
5. Continue iterating with the AI to refine your components

## Features

- AI-powered component generation using Claude
- Live preview with hot reload
- Virtual file system (no files written to disk)
- Syntax highlighting and code editor
- Component persistence for registered users
- Export generated code

## Tech Stack

- Next.js 15 with App Router
- React 19
- TypeScript
- Tailwind CSS v4
- Prisma with SQLite
- Anthropic Claude AI
- Vercel AI SDK

## API Documentation

UIGen provides a comprehensive RESTful API for component generation and management. For detailed API documentation, see [API.md](./API.md).

### Quick API Reference

**Authentication:**
- `POST /api/auth/signup` - Create user account
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - End session
- `POST /api/auth/anonymous` - Create anonymous session
- `GET /api/auth/session` - Get current session

**Component Generation:**
- `POST /api/generate` - Generate React component from text description

**Component Management:**
- `GET /api/components` - List all user components
- `GET /api/components/:id` - Get specific component
- `POST /api/components` - Save component
- `PUT /api/components/:id` - Update component
- `DELETE /api/components/:id` - Delete component

**Chat/Conversation:**
- `POST /api/chat` - Iterative component refinement (streaming)

**Export:**
- `POST /api/export` - Export component code (zip, json, files)

### Example Usage

```typescript
// Generate a component
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Create a responsive navigation bar with logo and menu items'
  })
});

const { component } = await response.json();
console.log(component.files);
```

For complete API documentation including request/response formats, error handling, rate limits, and SDK examples, see [API.md](./API.md).
