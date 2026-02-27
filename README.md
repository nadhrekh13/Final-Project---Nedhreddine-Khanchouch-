# Task Management API

A production-ready RESTful API for managing tasks, built with **FastAPI** and **Pydantic**.

## Features

- Full CRUD operations for tasks
- UUID-based task IDs
- Persistent storage via JSONL file
- Environment-based configuration
- Structured logging with timestamps
- Docker support

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- pip

### Manual Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Automated Setup

```bash
chmod +x run.sh
./run.sh
```

---

## Running the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## Running with Docker

```bash
# Build the image
docker build -t task-api .

# Run the container
docker run -p 8000:8000 task-api
```

---

## Configuration

The application is configured via environment variables (or a `.env` file):

| Variable        | Default          | Description                        |
|-----------------|------------------|------------------------------------|
| `ENVIRONMENT`   | `development`    | `development`, `testing`, or `production` |
| `HOST`          | `0.0.0.0`        | Host address for Uvicorn           |
| `PORT`          | `8000`           | Port for Uvicorn                   |
| `DATA_FILE`     | `tasks.jsonl`    | Path to the persistent data file   |
| `TEST_DATA_FILE`| `tasks_test.jsonl` | Data file used in testing        |

---

## API Endpoints

### List all tasks

```
GET /tasks
```

**Response:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }
]
```

---

### Create a task

```
POST /tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response:** `201 Created`

---

### Get a single task

```
GET /tasks/{task_id}
```

---

### Update a task

```
PUT /tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}
```

---

### Mark a task as completed

```
PATCH /tasks/{task_id}
```

---

### Delete a task

```
DELETE /tasks/{task_id}
```

---

### Get completed tasks

```
GET /tasks/completed
```

---

## Example curl Commands

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs"}'

# List all tasks
curl http://localhost:8000/tasks

# Get a single task
curl http://localhost:8000/tasks/<task_id>

# Update a task
curl -X PUT http://localhost:8000/tasks/<task_id> \
  -H "Content-Type: application/json" \
  -d '{"title": "New title"}'

# Mark as completed
curl -X PATCH http://localhost:8000/tasks/<task_id>

# Delete a task
curl -X DELETE http://localhost:8000/tasks/<task_id>

# Get completed tasks
curl http://localhost:8000/tasks/completed
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Project Structure

```
.
├── main.py          # FastAPI application and endpoints
├── config.py        # Environment-based configuration
├── requirements.txt # Python dependencies
├── Dockerfile       # Container definition
├── run.sh           # Setup and run script
├── tests/
│   ├── conftest.py  # Pytest fixtures
│   └── test_main.py # Test suite
└── .gitignore
```
