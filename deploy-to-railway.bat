@echo off
REM Railway Deployment Script for Tactics Master (Windows)
REM This script helps prepare and deploy your cricket analysis project to Railway

echo 🏏 Tactics Master - Railway Deployment Script
echo =============================================

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

echo [INFO] Starting Railway deployment preparation...

REM Step 1: Check if git is initialized
if not exist ".git" (
    echo [WARNING] Git repository not initialized. Initializing...
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
    echo [SUCCESS] Git repository initialized
) else (
    echo [SUCCESS] Git repository already initialized
)

REM Step 2: Check if railway.json exists
if not exist "railway.json" (
    echo [WARNING] railway.json not found. Please create it first.
    echo [ERROR] railway.json is required for Railway deployment
    pause
    exit /b 1
) else (
    echo [SUCCESS] railway.json already exists
)

REM Step 3: Check backend dependencies
echo [INFO] Checking backend dependencies...
cd backend

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in backend directory
    pause
    exit /b 1
) else (
    echo [SUCCESS] requirements.txt found
)

REM Step 4: Test backend import
echo [INFO] Testing backend import...
python -c "from main import app; print('✅ Backend app imports successfully')"
if %errorlevel% equ 0 (
    echo [SUCCESS] Backend app imports successfully
) else (
    echo [ERROR] Backend app import failed
    echo [WARNING] Make sure all dependencies are installed: pip install -r requirements.txt
    pause
    exit /b 1
)

cd ..

REM Step 5: Check environment variables
echo [INFO] Checking environment variables...
if exist ".env" (
    echo [SUCCESS] Environment file found
    echo [WARNING] Make sure to set environment variables in Railway dashboard
) else (
    echo [WARNING] No .env file found. Make sure to set environment variables in Railway dashboard
)

REM Step 6: Display deployment instructions
echo.
echo 🚀 Railway Deployment Instructions:
echo ===================================
echo.
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Prepare for Railway deployment"
echo    git push origin main
echo.
echo 2. Go to Railway Dashboard:
echo    https://railway.app/dashboard
echo.
echo 3. Create new project:
echo    - Click "New Project"
echo    - Select "Deploy from GitHub repo"
echo    - Choose your repository
echo.
echo 4. Configure backend service:
echo    - Railway will auto-detect the backend folder
echo    - If not, set Root Directory to "backend"
echo    - Railway will auto-configure Python and uvicorn
echo.
echo 5. Set environment variables in Railway:
echo    GEMINI_API_KEY=your_actual_gemini_api_key
echo    CRICKET_API_KEY=your_actual_cricket_api_key
echo    CRICKET_API_BASE_URL=https://api.cricketdata.org
echo.
echo 6. Deploy frontend (choose one):
echo    Option A: Add another service in Railway for frontend
echo    Option B: Deploy frontend to Netlify
echo.
echo 7. Update CORS settings in backend/main.py to include Railway domains
echo.

echo [SUCCESS] Deployment preparation complete!
echo [INFO] Follow the instructions above to complete the deployment

echo.
echo 📋 Required Environment Variables for Railway:
echo ==============================================
echo GEMINI_API_KEY=your_gemini_api_key_here
echo CRICKET_API_KEY=your_cricket_api_key_here
echo CRICKET_API_BASE_URL=https://api.cricketdata.org
echo.

echo 🔗 After deployment, you'll get:
echo ================================
echo Backend URL: https://your-backend-name.railway.app
echo API Docs: https://your-backend-name.railway.app/docs
echo Health Check: https://your-backend-name.railway.app/health

pause
