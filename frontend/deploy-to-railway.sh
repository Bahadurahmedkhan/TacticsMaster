#!/bin/bash

# Frontend deployment script for Railway
echo "🚀 Deploying Tactics Master Frontend to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
railway whoami || railway login

# Create new project or link to existing
echo "📦 Setting up Railway project..."
railway link

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "Please enter your backend URL (e.g., https://your-backend.railway.app):"
read -p "Backend URL: " BACKEND_URL

railway variables set REACT_APP_API_URL=$BACKEND_URL
railway variables set GENERATE_SOURCEMAP=false
railway variables set NODE_ENV=production

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your frontend should be available at the Railway URL"
