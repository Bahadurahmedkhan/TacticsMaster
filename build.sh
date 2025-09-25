#!/bin/bash

# Build script for Railway deployment
echo "Starting Railway deployment..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the application
echo "Building React app..."
npm run build

# Install serve globally
echo "Installing serve..."
npm install -g serve

# Start the application
echo "Starting application..."
serve -s build -l $PORT
