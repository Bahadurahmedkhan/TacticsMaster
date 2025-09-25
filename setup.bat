@echo off
echo 🏏 Setting up Tactics Master Agent...

echo.
echo 📦 Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo 📦 Installing Frontend Dependencies...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Copy backend\env.example to backend\.env and add your API keys
echo 2. Copy frontend\env.example to frontend\.env
echo 3. Run start_backend.bat to start the backend server
echo 4. Run start_frontend.bat to start the frontend
echo.
pause
