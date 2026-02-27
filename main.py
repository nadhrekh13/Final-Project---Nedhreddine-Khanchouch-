import json
import logging
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import settings

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Pydantic models
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


# In-memory storage for tasks
tasks: List[dict] = []


# Helper functions for loading and saving tasks
def load_tasks() -> None:
    global tasks
    try:
        with open(settings.data_file, "r") as f:
            loaded = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    loaded.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning("Skipping malformed JSON line in %s: %s", settings.data_file, exc)
            tasks = loaded
        logger.info("Loaded %d task(s) from %s", len(tasks), settings.data_file)
    except FileNotFoundError:
        tasks = []
        logger.info("No data file found at %s; starting with empty task list", settings.data_file)


def save_tasks() -> None:
    with open(settings.data_file, "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")
    logger.debug("Saved %d task(s) to %s", len(tasks), settings.data_file)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_tasks()
    yield


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)


# Endpoints
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    logger.info("Fetching all tasks")
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=422, detail="Task title must not be empty")
    task_id = str(uuid.uuid4())
    new_task = {**task.model_dump(), "id": task_id, "completed": False}
    tasks.append(new_task)
    save_tasks()
    logger.info("Created task %s: %s", task_id, task.title)
    return new_task


@app.get("/tasks/completed", response_model=List[Task])
def get_completed_tasks():
    logger.info("Fetching completed tasks")
    return [task for task in tasks if task["completed"]]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    for task in tasks:
        if task["id"] == task_id:
            return task
    logger.warning("Task %s not found", task_id)
    raise HTTPException(status_code=404, detail=f"Task with id '{task_id}' not found")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=422, detail="Task title must not be empty")
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i].update(task.model_dump())
            save_tasks()
            logger.info("Updated task %s", task_id)
            return tasks[i]
    logger.warning("Task %s not found", task_id)
    raise HTTPException(status_code=404, detail=f"Task with id '{task_id}' not found")


@app.patch("/tasks/{task_id}", response_model=Task)
def complete_task(task_id: str):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i]["completed"] = True
            save_tasks()
            logger.info("Marked task %s as completed", task_id)
            return tasks[i]
    logger.warning("Task %s not found", task_id)
    raise HTTPException(status_code=404, detail=f"Task with id '{task_id}' not found")


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks()
            logger.info("Deleted task %s", task_id)
            return {"message": "Task deleted successfully", "task": deleted_task}
    logger.warning("Task %s not found", task_id)
    raise HTTPException(status_code=404, detail=f"Task with id '{task_id}' not found")

