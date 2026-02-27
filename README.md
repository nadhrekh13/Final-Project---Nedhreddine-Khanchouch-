# Task Management API Documentation

## Overview
This is a comprehensive guide for the Task Management API, designed to help developers integrate and utilize the API effectively.

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadhrekh13/Final-Project---Nedhreddine-Khanchouch-
   cd Final-Project---Nedhreddine-Khanchouch-
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the server:**
   ```bash
   npm start
   ```

## API Endpoints

### 1. Create a Task
- **Endpoint:** `POST /api/tasks`
- **Request Body:**
   ```json
   {
      "title": "Task Title",
      "description": "Task Description",
      "dueDate": "2026-02-27T11:00:00Z"
   }
   ```
- **Response:**
   ```json
   {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "dueDate": "2026-02-27T11:00:00Z",
      "status": "pending"
   }
   ```

### 2. Get All Tasks
- **Endpoint:** `GET /api/tasks`
- **Response:**
   ```json
   [
      {
         "id": 1,
         "title": "Task Title",
         "description": "Task Description",
         "dueDate": "2026-02-27T11:00:00Z",
         "status": "pending"
      }
   ]
   ```

### 3. Get a Task by ID
- **Endpoint:** `GET /api/tasks/{id}`
- **Response:**
   ```json
   {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "dueDate": "2026-02-27T11:00:00Z",
      "status": "pending"
   }
   ```

### 4. Update a Task
- **Endpoint:** `PUT /api/tasks/{id}`
- **Request Body:**
   ```json
   {
      "title": "Updated Task Title",
      "description": "Updated Task Description",
      "status": "completed"
   }
   ```
- **Response:**
   ```json
   {
      "id": 1,
      "title": "Updated Task Title",
      "description": "Updated Task Description",
      "dueDate": "2026-02-27T11:00:00Z",
      "status": "completed"
   }
   ```

### 5. Delete a Task
- **Endpoint:** `DELETE /api/tasks/{id}`
- **Response:**
   ```json
   {
      "message": "Task successfully deleted"
   }
   ```

### 6. Get Task by Status
- **Endpoint:** `GET /api/tasks?status={status}`
- **Response:**
   ```json
   [
      {
         "id": 1,
         "title": "Task Title",
         "description": "Task Description",
         "dueDate": "2026-02-27T11:00:00Z",
         "status": "pending"
      }
   ]
   ```

### 7. Update Task Status
- **Endpoint:** `PATCH /api/tasks/{id}/status`
- **Request Body:**
   ```json
   {
      "status": "completed"
   }
   ```
- **Response:**
   ```json
   {
      "id": 1,
      "status": "completed"
   }
   ```

### 8. Bulk Create Tasks
- **Endpoint:** `POST /api/tasks/bulk`
- **Request Body:**
   ```json
   [
      {
         "title": "Task 1",
         "description": "Description 1"
      },
      {
         "title": "Task 2",
         "description": "Description 2"
      }
   ]
   ```
- **Response:**
   ```json
   [
      {
         "id": 1,
         "title": "Task 1"
      },
      {
         "id": 2,
         "title": "Task 2"
      }
   ]
   ```

### 9. Get Overdue Tasks
- **Endpoint:** `GET /api/tasks/overdue`
- **Response:**
   ```json
   [
      {
         "id": 1,
         "title": "Overdue Task",
         "description": "Description",
         "dueDate": "2026-02-20T11:00:00Z",
         "status": "pending"
      }
   ]
   ```

## Task Data Model
```json
{
   "id": 1,
   "title": "Task Title",
   "description": "Task Description",
   "dueDate": "2026-02-27T11:00:00Z",
   "status": "pending"
}
```

## Project Structure
```
Final-Project---Nedhreddine-Khanchouch/
├── api/
│   └── tasks.js
├── models/
│   └── task.js
├── routes/
│   └── taskRoutes.js
├── server.js
└── package.json
```

## Error Handling
- **400 Bad Request:** Invalid input data.
- **404 Not Found:** Task not found.
- **500 Internal Server Error:** Server encountered an error.

## Submission Requirements
- Ensure all endpoints are tested and documented.
- Code should follow best practices and be well-commented.
- Submit via GitHub with a clear description of changes made.