# Flask API

A simple Flask API with health check and echo endpoints.

## Prerequisites

- Python 3.7+
- pip

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /health

Health check endpoint that returns the API status.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

### POST /echo

Echo endpoint that returns the data sent in the request body.

**Request Body:** JSON data

**Response:**
```json
{
  "echoed": <your-data>
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!"}'
```

## Tech Stack

- Flask 3.0.0
- Python
