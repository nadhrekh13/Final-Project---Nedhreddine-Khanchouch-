import json
import os


def load_tasks():
    """
    Load tasks from the tasks.txt file.
    Returns an empty list if the file doesn't exist.
    Each line in the file is a JSON object representing a task.
    """
    if not os.path.exists("tasks.txt"):
        return []
    
    tasks = []
    with open("tasks.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    task = json.loads(line)
                    tasks.append(task)
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
    
    return tasks


def save_tasks(tasks):
    """
    Save tasks to the tasks.txt file.
    Each task is written as a JSON object on a separate line (JSON Lines format).
    """
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")
