#!/usr/bin/env python3
"""
Test script to verify the backend is working
"""

import requests
import time
import subprocess
import sys
import os

def test_backend():
    """Test the backend endpoints"""
    
    # Start the backend server
    print("Starting backend server...")
    process = subprocess.Popen([
        sys.executable, "-c", 
        "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"
    ])
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        
        # Test analyze endpoint
        print("\nTesting analyze endpoint...")
        test_data = {
            "query": "How should I set my field for a new batsman?",
            "context": {}
        }
        
        response = requests.post(
            "http://localhost:8000/analyze", 
            json=test_data, 
            timeout=30
        )
        
        print(f"Analyze endpoint status: {response.status_code}")
        print(f"Analyze endpoint response: {response.json()}")
        
        print("\n✅ Backend is working correctly!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_backend()
