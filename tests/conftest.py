import pytest
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
import main
from fastapi.testclient import TestClient

@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with an isolated temporary tasks file."""
    tasks_file = str(tmp_path / "tasks.jsonl")
    monkeypatch.setattr(config, "TASKS_FILE", tasks_file)
    main.tasks.clear()
    with TestClient(main.app) as c:
        yield c
    main.tasks.clear()

@pytest.fixture
def sample_task(client):
    response = client.post('/tasks', json={'title': 'Test Task', 'description': 'A test task'})
    assert response.status_code == 201
    return response.json()
