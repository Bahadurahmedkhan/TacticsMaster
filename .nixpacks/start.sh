#!/bin/bash

# Nixpacks start script for frontend
echo "Starting frontend application..."

# Navigate to frontend directory
cd frontend

# Start the application
serve -s build -l $PORT
