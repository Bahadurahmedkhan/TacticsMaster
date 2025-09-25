@echo off
echo 🚀 Deploying Tactics Master Frontend to Railway...

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Please install it first:
    echo npm install -g @railway/cli
    pause
    exit /b 1
)

REM Login to Railway (if not already logged in)
echo 🔐 Checking Railway authentication...
railway whoami
if %errorlevel% neq 0 (
    railway login
)

REM Create new project or link to existing
echo 📦 Setting up Railway project...
railway link

REM Set environment variables
echo 🔧 Setting up environment variables...
set /p BACKEND_URL="Please enter your backend URL (e.g., https://your-backend.railway.app): "

railway variables set REACT_APP_API_URL=%BACKEND_URL%
railway variables set GENERATE_SOURCEMAP=false
railway variables set NODE_ENV=production

REM Deploy
echo 🚀 Deploying to Railway...
railway up

echo ✅ Deployment complete!
echo 🌐 Your frontend should be available at the Railway URL
pause
