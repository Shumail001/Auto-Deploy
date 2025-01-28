#!/bin/bash
# Navigate to the app directory
# shellcheck disable=SC2164
cd /home/ubuntu/app/

# Stop the existing process (if running)
pkill -f "uvicorn"

# Start the FastAPI app using Uvicorn on port 8000
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
