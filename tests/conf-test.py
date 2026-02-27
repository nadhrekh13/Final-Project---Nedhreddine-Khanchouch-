import os
import pytest
from fastapi.testclient import TestClient

# Set testing environment before importing the app
os.environ["ENVIRONMENT"] = "testing"

import main as main_module  # noqa: E402  (import after env var is set)
import config  # noqa: E402
from main import app


@pytest.fixture(autouse=True)
def clear_tasks(tmp_path, monkeypatch):
    """Reset the in-memory task list and redirect data file to a temp location before each test."""
    monkeypatch.setattr(config.settings, "TEST_DATA_FILE", str(tmp_path / "tasks_test.jsonl"))
    main_module.tasks.clear()
    yield
    main_module.tasks.clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
