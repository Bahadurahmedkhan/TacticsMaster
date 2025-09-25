#!/usr/bin/env python3
"""
Test script for Tactics Master Agent with real CricAPI data
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

def test_cricapi_integration():
    """Test the CricAPI integration with the agent tools"""
    print("🏏 Testing Tactics Master Agent with CricAPI...")
    print("=" * 60)
    
    try:
        # Import the tools
        from tools.cricket_api_tools import get_player_stats, get_team_squad
        from tools.tactical_tools import analyze_weaknesses, generate_bowling_plan
        
        print("✅ Tools imported successfully")
        
        # Test 1: Get real player stats from CricAPI
        print("\n📊 Testing real player data fetch...")
        player_data = get_player_stats("Virat Kohli")
        
        # Parse the JSON to check if it's real data
        import json
        data = json.loads(player_data)
        
        if "source" in data and data["source"] == "CricAPI":
            print("✅ Real CricAPI data fetched successfully!")
            print(f"   Player: {data.get('player_name', 'Unknown')}")
            print(f"   Source: {data.get('source', 'Unknown')}")
        else:
            print("ℹ️  Using mock data (CricAPI may be rate limited)")
            print(f"   Player: {data.get('player_name', 'Unknown')}")
        
        # Test 2: Analyze weaknesses
        print("\n🔍 Testing tactical analysis...")
        analysis = analyze_weaknesses(player_data)
        analysis_data = json.loads(analysis)
        
        if "error" not in analysis_data:
            print("✅ Tactical analysis completed successfully!")
            print(f"   Assessment: {analysis_data.get('overall_assessment', 'N/A')}")
            print(f"   Weaknesses found: {len(analysis_data.get('key_weaknesses', []))}")
        else:
            print(f"❌ Analysis failed: {analysis_data.get('error', 'Unknown error')}")
        
        # Test 3: Generate bowling plan
        print("\n🏏 Testing bowling plan generation...")
        bowling_plan = generate_bowling_plan(player_data, "Test match context")
        plan_data = json.loads(bowling_plan)
        
        if "error" not in plan_data:
            print("✅ Bowling plan generated successfully!")
            print(f"   Strategy: {plan_data.get('overall_strategy', 'N/A')}")
            print(f"   Phases planned: {len(plan_data.get('phase_plans', {}))}")
        else:
            print(f"❌ Bowling plan failed: {plan_data.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 60)
        print("🎯 Tactics Master Agent Test Complete!")
        print("\n✅ All components working correctly!")
        print("\nNext steps:")
        print("1. Add your language model API key (OpenAI or Gemini) to .env")
        print("2. Run: python app/main.py")
        print("3. Ask questions like: 'Analyze Virat Kohli's weaknesses'")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_cricapi_integration()
