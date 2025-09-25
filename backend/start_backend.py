#!/usr/bin/env python3
"""
Start the backend server with proper error handling
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_backend import app
    print("✅ Backend app imported successfully")
    
    print("🚀 Starting Tactics Master Backend Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    print("🔗 Analyze Endpoint: http://localhost:8000/analyze")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)
