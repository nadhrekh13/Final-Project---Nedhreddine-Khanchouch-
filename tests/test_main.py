"""Unit tests for all CRUD endpoints in main.py."""
import pytest


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------

def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_returns_all(client):
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------

def test_create_task_minimal(client):
    response = client.post("/tasks", json={"title": "Buy groceries"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] is None
    assert data["completed"] is False
    assert "id" in data


def test_create_task_with_description(client):
    response = client.post(
        "/tasks", json={"title": "Read book", "description": "Finish chapter 3"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Finish chapter 3"


def test_create_task_ids_are_unique(client):
    r1 = client.post("/tasks", json={"title": "Task 1"})
    r2 = client.post("/tasks", json={"title": "Task 2"})
    assert r1.json()["id"] != r2.json()["id"]


def test_create_task_empty_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /tasks/{task_id}
# ---------------------------------------------------------------------------

def test_get_task_by_id(client):
    created = client.post("/tasks", json={"title": "Single task"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_not_found(client):
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /tasks/{task_id}
# ---------------------------------------------------------------------------

def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old title"}).json()
    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "New title", "description": "Updated"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["description"] == "Updated"


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/nonexistent-id", json={"title": "Doesn't matter"}
    )
    assert response.status_code == 404


def test_update_task_empty_title(client):
    created = client.post("/tasks", json={"title": "Valid"}).json()
    response = client.put(f"/tasks/{created['id']}", json={"title": "  "})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /tasks/{task_id}  (mark as completed)
# ---------------------------------------------------------------------------

def test_complete_task(client):
    created = client.post("/tasks", json={"title": "Do laundry"}).json()
    response = client.patch(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_task_not_found(client):
    response = client.patch("/tasks/nonexistent-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /tasks/{task_id}
# ---------------------------------------------------------------------------

def test_delete_task(client):
    created = client.post("/tasks", json={"title": "To delete"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert "Task deleted successfully" in response.json()["message"]

    # Confirm it's gone
    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /tasks/completed
# ---------------------------------------------------------------------------

def test_get_completed_tasks_empty(client):
    client.post("/tasks", json={"title": "Incomplete task"})
    response = client.get("/tasks/completed")
    assert response.status_code == 200
    assert response.json() == []


def test_get_completed_tasks(client):
    t1 = client.post("/tasks", json={"title": "Task 1"}).json()
    client.post("/tasks", json={"title": "Task 2"})
    client.patch(f"/tasks/{t1['id']}")

    response = client.get("/tasks/completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == t1["id"]
    assert data[0]["completed"] is True
