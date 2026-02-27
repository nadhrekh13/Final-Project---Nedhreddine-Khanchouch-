import os

# API settings
APP_TITLE = "Task Management API"
APP_DESCRIPTION = "A simple task management API built with FastAPI"
APP_VERSION = "1.0.0"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Storage settings
TASKS_FILE = os.getenv("TASKS_FILE", "tasks.jsonl")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
