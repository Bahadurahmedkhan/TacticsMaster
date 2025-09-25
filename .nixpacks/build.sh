#!/bin/bash

# Nixpacks build script for frontend
echo "Building frontend with Nixpacks..."

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

echo "Build completed successfully!"
