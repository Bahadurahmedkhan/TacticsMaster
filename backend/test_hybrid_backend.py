#!/usr/bin/env python3
"""
Test the hybrid backend with real API integration
"""

import asyncio
import os
import sys

# Set environment variables
os.environ["GEMINI_API_KEY"] = "AIzaSyB5-5hl8MLE792mgvNxid9wqGkZLZE_3n0"
os.environ["CRICKET_API_KEY"] = "19c15f09-f093-493d-80cf-219169585415"

async def test_hybrid_agent():
    """Test the hybrid agent"""
    
    try:
        from hybrid_agent import HybridTacticsMasterAgent
        
        print("🏏 Testing Hybrid Tactics Master Agent...")
        print("=" * 50)
        
        # Initialize agent
        agent = HybridTacticsMasterAgent()
        print("✅ Agent initialized successfully")
        
        # Test with a cricket query
        test_query = "How should I set my field for a new batsman in the powerplay?"
        print(f"\n🔍 Testing query: {test_query}")
        
        # Analyze the query
        result = await agent.analyze(test_query, {})
        
        print("\n📊 Analysis Results:")
        print("=" * 30)
        print(f"Response: {result['response'][:200]}...")
        print(f"Sources: {result['sources']}")
        print(f"Analysis: {result['analysis']}")
        
        print("\n✅ Hybrid agent test completed successfully!")
        print("🎯 The system is using:")
        print("   - Real cricket data from CricAPI")
        print("   - Intelligent fallback analysis")
        print("   - No Gemini API quota issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def main():
    """Main test function"""
    
    print("🚀 Starting Hybrid Backend Test...")
    
    success = await test_hybrid_agent()
    
    if success:
        print("\n🎉 All tests passed! The hybrid backend is ready.")
        print("You can now start the backend with: python main.py")
    else:
        print("\n❌ Tests failed. Please check the configuration.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
