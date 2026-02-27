"""Unit and integration tests for the Task Management API.

Covers all CRUD endpoints: create, read, update, delete, complete, and
filtering by completion status. Each test uses the `client` fixture which
provides an isolated FastAPI TestClient with a temporary tasks file so
tests do not interfere with each other.
"""


def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Buy groceries', 'description': 'Milk and eggs'})
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Buy groceries'
    assert data['description'] == 'Milk and eggs'
    assert data['completed'] is False
    assert 'id' in data
    assert isinstance(data['id'], str)


def test_create_task_no_description(client):
    response = client.post('/tasks', json={'title': 'Simple task'})
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Simple task'
    assert data['description'] is None


def test_create_task_missing_title(client):
    response = client.post('/tasks', json={'description': 'No title'})
    assert response.status_code == 422


def test_get_tasks_after_create(client):
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client, sample_task):
    task_id = sample_task['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['id'] == task_id


def test_get_task_not_found(client):
    response = client.get('/tasks/nonexistent-id')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


def test_update_task(client, sample_task):
    task_id = sample_task['id']
    response = client.put(f'/tasks/{task_id}', json={'title': 'Updated Title', 'description': 'Updated desc'})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Updated Title'
    assert data['description'] == 'Updated desc'


def test_update_task_not_found(client):
    response = client.put('/tasks/nonexistent-id', json={'title': 'X'})
    assert response.status_code == 404


def test_complete_task(client, sample_task):
    task_id = sample_task['id']
    response = client.patch(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['completed'] is True


def test_complete_task_not_found(client):
    response = client.patch('/tasks/nonexistent-id')
    assert response.status_code == 404


def test_delete_task(client, sample_task):
    task_id = sample_task['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'Task deleted'
    # Verify it's gone
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete('/tasks/nonexistent-id')
    assert response.status_code == 404


def test_get_completed_tasks_empty(client):
    client.post('/tasks', json={'title': 'Incomplete task'})
    response = client.get('/tasks/completed')
    assert response.status_code == 200
    assert response.json() == []


def test_get_completed_tasks(client):
    resp1 = client.post('/tasks', json={'title': 'Task 1'})
    resp2 = client.post('/tasks', json={'title': 'Task 2'})
    task_id1 = resp1.json()['id']
    client.patch(f'/tasks/{task_id1}')
    response = client.get('/tasks/completed')
    assert response.status_code == 200
    completed = response.json()
    assert len(completed) == 1
    assert completed[0]['id'] == task_id1


def test_task_ids_are_unique(client):
    ids = set()
    for i in range(5):
        resp = client.post('/tasks', json={'title': f'Task {i}'})
        ids.add(resp.json()['id'])
    assert len(ids) == 5
