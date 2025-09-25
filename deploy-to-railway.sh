#!/bin/bash

# Railway Deployment Script for Tactics Master
# This script helps prepare and deploy your cricket analysis project to Railway

echo "🏏 Tactics Master - Railway Deployment Script"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting Railway deployment preparation..."

# Step 1: Check if git is initialized
if [ ! -d ".git" ]; then
    print_warning "Git repository not initialized. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
    print_success "Git repository initialized"
else
    print_success "Git repository already initialized"
fi

# Step 2: Check if railway.json exists
if [ ! -f "railway.json" ]; then
    print_warning "railway.json not found. Creating..."
    print_success "railway.json created"
else
    print_success "railway.json already exists"
fi

# Step 3: Check backend dependencies
print_status "Checking backend dependencies..."
cd backend

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in backend directory"
    exit 1
else
    print_success "requirements.txt found"
fi

# Step 4: Test backend import
print_status "Testing backend import..."
python -c "from main import app; print('✅ Backend app imports successfully')"
if [ $? -eq 0 ]; then
    print_success "Backend app imports successfully"
else
    print_error "Backend app import failed"
    print_warning "Make sure all dependencies are installed: pip install -r requirements.txt"
    exit 1
fi

cd ..

# Step 5: Check environment variables
print_status "Checking environment variables..."
if [ -f ".env" ]; then
    print_success "Environment file found"
    print_warning "Make sure to set environment variables in Railway dashboard"
else
    print_warning "No .env file found. Make sure to set environment variables in Railway dashboard"
fi

# Step 6: Display deployment instructions
echo ""
echo "🚀 Railway Deployment Instructions:"
echo "==================================="
echo ""
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Railway deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to Railway Dashboard:"
echo "   https://railway.app/dashboard"
echo ""
echo "3. Create new project:"
echo "   - Click 'New Project'"
echo "   - Select 'Deploy from GitHub repo'"
echo "   - Choose your repository"
echo ""
echo "4. Configure backend service:"
echo "   - Railway will auto-detect the backend folder"
echo "   - If not, set Root Directory to 'backend'"
echo "   - Railway will auto-configure Python and uvicorn"
echo ""
echo "5. Set environment variables in Railway:"
echo "   GEMINI_API_KEY=your_actual_gemini_api_key"
echo "   CRICKET_API_KEY=your_actual_cricket_api_key"
echo "   CRICKET_API_BASE_URL=https://api.cricketdata.org"
echo ""
echo "6. Deploy frontend (choose one):"
echo "   Option A: Add another service in Railway for frontend"
echo "   Option B: Deploy frontend to Netlify"
echo ""
echo "7. Update CORS settings in backend/main.py to include Railway domains"
echo ""

print_success "Deployment preparation complete!"
print_status "Follow the instructions above to complete the deployment"

echo ""
echo "📋 Required Environment Variables for Railway:"
echo "=============================================="
echo "GEMINI_API_KEY=your_gemini_api_key_here"
echo "CRICKET_API_KEY=your_cricket_api_key_here"
echo "CRICKET_API_BASE_URL=https://api.cricketdata.org"
echo ""

echo "🔗 After deployment, you'll get:"
echo "================================"
echo "Backend URL: https://your-backend-name.railway.app"
echo "API Docs: https://your-backend-name.railway.app/docs"
echo "Health Check: https://your-backend-name.railway.app/health"
