#!/usr/bin/env python3
"""
Start the backend server with real API integration
"""

import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_keys():
    """Check if API keys are available"""
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    cricket_key = os.getenv("CRICKET_API_KEY")
    
    if not gemini_key or gemini_key == "your_actual_gemini_api_key_here":
        print("❌ Gemini API key not found!")
        print("Please set GEMINI_API_KEY environment variable or run setup_api_keys.py")
        return False
    
    if not cricket_key or cricket_key == "your_actual_cricapi_key_here":
        print("❌ Cricket API key not found!")
        print("Please set CRICKET_API_KEY environment variable or run setup_api_keys.py")
        return False
    
    return True

def main():
    """Start the backend server"""
    
    print("🏏 Starting Tactics Master Agent with Real APIs...")
    print("=" * 50)
    
    # Check API keys
    if not check_api_keys():
        print("\n💡 To set up API keys, run: python setup_api_keys.py")
        sys.exit(1)
    
    try:
        # Import the main app
        from main import app
        
        print("✅ Backend app imported successfully")
        print("🚀 Starting server with real API integration...")
        print("📊 API Documentation: http://localhost:8000/docs")
        print("🔗 Health Check: http://localhost:8000/health")
        print("🔗 Analyze Endpoint: http://localhost:8000/analyze")
        print("\n🎯 The system will now use:")
        print("   - Gemini AI for tactical analysis")
        print("   - CricAPI for real cricket data")
        print("   - LangChain for agent orchestration")
        
        # Start the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
