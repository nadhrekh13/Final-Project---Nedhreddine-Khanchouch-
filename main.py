from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI()

# Pydantic models
class Task(BaseModel):
    id: int
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
        with open('tasks.jsonl', 'r') as f:
            tasks = [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        tasks = []

def save_tasks():
    with open('tasks.jsonl', 'w') as f:
        for task in tasks:
            f.write(json.dumps(task) + '\n')

# Load tasks on startup
load_tasks()

# Endpoints
@app.get('/tasks', response_model=List[Task])
def get_tasks():
    return tasks

@app.post('/tasks', response_model=Task)
def create_task(task: TaskCreate):
    task_id = len(tasks) + 1
    new_task = {**task.dict(), 'id': task_id, 'completed': False}
    tasks.append(new_task)
    save_tasks()
    return new_task

@app.get('/tasks/{task_id}', response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            tasks[i].update(task.dict())
            save_tasks()
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/tasks/{task_id}', response_model=dict)
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks()
            return {'message': 'Task deleted', 'task': deleted_task}
    raise HTTPException(status_code=404, detail='Task not found')

@app.get('/tasks/completed', response_model=List[Task])
def get_completed_tasks():
    completed_tasks = [task for task in tasks if task['completed']]
    return completed_tasks

@app.patch('/tasks/{task_id}', response_model=Task)
def complete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            tasks[i]['completed'] = True
            save_tasks()
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')

