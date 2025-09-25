#!/usr/bin/env python3
"""
Start the hybrid backend with the new API key
"""

import os
import uvicorn
import sys

# Set environment variables (use your own API keys)
# os.environ["GEMINI_API_KEY"] = "your_gemini_api_key_here"
# os.environ["CRICKET_API_KEY"] = "your_cricket_api_key_here"

def main():
    """Start the hybrid backend server"""
    
    print("🏏 Starting Tactics Master Agent with New API Key...")
    print("=" * 60)
    print("🔑 Using Gemini Flash model with new API key")
    print("📊 Real cricket data from CricAPI")
    print("🧠 AI-powered tactical analysis")
    print("=" * 60)
    
    try:
        # Import the main app
        from main import app
        
        print("✅ Backend app imported successfully")
        print("🚀 Starting server...")
        print("📊 API Documentation: http://localhost:8000/docs")
        print("🔗 Health Check: http://localhost:8000/health")
        print("🔗 Analyze Endpoint: http://localhost:8000/analyze")
        print("\n🎯 The system is now using:")
        print("   - Gemini Flash AI for analysis")
        print("   - Real cricket data from CricAPI")
        print("   - API keys from environment variables")
        
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
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
