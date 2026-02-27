#!/usr/bin/env bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting Task Management API..."
uvicorn main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}" --reload
