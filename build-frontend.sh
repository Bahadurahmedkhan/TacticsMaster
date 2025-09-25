#!/bin/bash

# Build script for frontend deployment
echo "Building frontend..."

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the application
npm run build

# Install serve globally
npm install -g serve

# Start the application
serve -s build -l $PORT
