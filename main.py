import logging
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL, logging.INFO))
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
tasks = []

# Helper functions for loading and saving tasks
def load_tasks():
    global tasks
    try:
        with open(config.TASKS_FILE, 'r') as f:
            tasks = [json.loads(line) for line in f if line.strip()]
        logger.info("Loaded %d tasks from %s", len(tasks), config.TASKS_FILE)
    except FileNotFoundError:
        tasks = []
        logger.info("No existing tasks file found, starting fresh")

def save_tasks():
    with open(config.TASKS_FILE, 'w') as f:
        for task in tasks:
            f.write(json.dumps(task) + '\n')

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_tasks()
    logger.info("Application started")
    yield
    save_tasks()
    logger.info("Application shutdown")

app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    lifespan=lifespan,
)

# Endpoints
@app.get('/tasks', response_model=List[Task])
def get_tasks():
    return tasks

@app.get('/tasks/completed', response_model=List[Task])
def get_completed_tasks():
    return [task for task in tasks if task['completed']]

@app.post('/tasks', response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = {**task.model_dump(), 'id': str(uuid.uuid4()), 'completed': False}
    tasks.append(new_task)
    save_tasks()
    logger.info("Created task %s", new_task['id'])
    return new_task

@app.get('/tasks/{task_id}', response_model=Task)
def get_task(task_id: str):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: str, task: TaskCreate):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            tasks[i].update(task.model_dump())
            save_tasks()
            logger.info("Updated task %s", task_id)
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')

@app.patch('/tasks/{task_id}', response_model=Task)
def complete_task(task_id: str):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            tasks[i]['completed'] = True
            save_tasks()
            logger.info("Marked task %s as completed", task_id)
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/tasks/{task_id}', response_model=dict)
def delete_task(task_id: str):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks()
            logger.info("Deleted task %s", task_id)
            return {'message': 'Task deleted', 'task': deleted_task}
    raise HTTPException(status_code=404, detail='Task not found')

