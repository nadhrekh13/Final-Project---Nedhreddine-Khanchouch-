# Task Management API

A simple, production-ready task management REST API built with [FastAPI](https://fastapi.tiangolo.com/) and Python.

## Features

- Create, read, update, and delete tasks (CRUD)
- Mark tasks as completed
- Filter completed tasks
- Persistent storage via JSONL file
- UUID-based task IDs
- Structured logging
- Fully tested with pytest

## Project Structure

```
.
├── main.py          # FastAPI application and endpoints
├── config.py        # Configuration management
├── requirements.txt # Python dependencies
├── run.sh           # Setup and run script
├── Dockerfile       # Docker container definition
├── tests/
│   ├── conftest.py  # Shared test fixtures
│   └── test_tasks.py# Test suite
└── README.md
```

## Requirements

- Python 3.10+
- pip

## Installation & Setup

### Option 1: Using run.sh

```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Docker

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

## Configuration

The following environment variables are supported:

| Variable    | Default       | Description                      |
|-------------|---------------|----------------------------------|
| HOST        | 0.0.0.0       | Host to bind to                  |
| PORT        | 8000          | Port to listen on                |
| DEBUG       | false         | Enable debug mode                |
| TASKS_FILE  | tasks.jsonl   | Path to the task storage file    |
| LOG_LEVEL   | INFO          | Logging level                    |

## API Endpoints

The interactive API documentation is available at `http://localhost:8000/docs` after starting the server.

### Endpoints

| Method | Path                   | Description               |
|--------|------------------------|---------------------------|
| GET    | `/tasks`               | List all tasks            |
| POST   | `/tasks`               | Create a new task         |
| GET    | `/tasks/completed`     | List completed tasks      |
| GET    | `/tasks/{task_id}`     | Get a specific task       |
| PUT    | `/tasks/{task_id}`     | Update a task             |
| PATCH  | `/tasks/{task_id}`     | Mark a task as completed  |
| DELETE | `/tasks/{task_id}`     | Delete a task             |

### Example Usage

**Create a task:**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**List all tasks:**
```bash
curl http://localhost:8000/tasks
```

**Mark a task as completed:**
```bash
curl -X PATCH http://localhost:8000/tasks/<task_id>
```

**Delete a task:**
```bash
curl -X DELETE http://localhost:8000/tasks/<task_id>
```

## Running Tests

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## License

This project is for educational purposes.
