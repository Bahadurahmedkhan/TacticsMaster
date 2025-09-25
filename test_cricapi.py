#!/usr/bin/env python3
"""
Test script for CricAPI integration
This script tests the CricAPI connection and fetches real cricket data
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CricAPI Configuration
CRICAPI_KEY = "19c15f09-f093-493d-80cf-219169585415"
CRICAPI_BASE = "https://api.cricapi.com/v1"

def test_cricapi_connection():
    """Test CricAPI connection and fetch sample data"""
    print("🏏 Testing CricAPI Connection...")
    print(f"API Key: {CRICAPI_KEY[:8]}...{CRICAPI_KEY[-8:]}")
    print("-" * 50)
    
    try:
        # Test 1: Get current matches
        print("📊 Fetching current matches...")
        matches_url = f"{CRICAPI_BASE}/currentMatches"
        params = {"apikey": CRICAPI_KEY}
        
        response = requests.get(matches_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Connection Successful!")
            print(f"Status: {data.get('status', 'Unknown')}")
            print(f"Data Available: {data.get('data', [])}")
            
            if data.get('data'):
                print(f"📈 Found {len(data['data'])} current matches")
                for match in data['data'][:3]:  # Show first 3 matches
                    print(f"  - {match.get('name', 'Unknown Match')}")
                    print(f"    Status: {match.get('status', 'Unknown')}")
            else:
                print("ℹ️  No current matches found")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    try:
        # Test 2: Search for a player
        print("\n🔍 Testing player search...")
        search_url = f"{CRICAPI_BASE}/players"
        params = {
            "apikey": CRICAPI_KEY,
            "search": "Virat Kohli"
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Player Search Successful!")
            print(f"Status: {data.get('status', 'Unknown')}")
            
            if data.get('data'):
                print(f"📈 Found {len(data['data'])} players")
                for player in data['data'][:3]:  # Show first 3 players
                    print(f"  - {player.get('name', 'Unknown Player')}")
                    print(f"    ID: {player.get('id', 'Unknown')}")
            else:
                print("ℹ️  No players found")
        else:
            print(f"❌ Player Search Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Player Search Error: {e}")
        return False
    
    return True

def test_player_stats():
    """Test fetching detailed player statistics"""
    print("\n📊 Testing player statistics...")
    
    try:
        # First, search for a player to get their ID
        search_url = f"{CRICAPI_BASE}/players"
        params = {
            "apikey": CRICAPI_KEY,
            "search": "Virat Kohli"
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                player_id = data['data'][0]['id']
                player_name = data['data'][0]['name']
                
                print(f"✅ Found player: {player_name} (ID: {player_id})")
                
                # Get detailed player stats
                stats_url = f"{CRICAPI_BASE}/players/{player_id}"
                stats_response = requests.get(stats_url, params={"apikey": CRICAPI_KEY}, timeout=10)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    print(f"✅ Player stats retrieved successfully!")
                    print(f"Status: {stats_data.get('status', 'Unknown')}")
                    
                    # Show some key stats
                    if stats_data.get('data'):
                        player_data = stats_data['data']
                        print(f"📈 Player Statistics:")
                        print(f"  - Name: {player_data.get('name', 'Unknown')}")
                        print(f"  - Country: {player_data.get('country', 'Unknown')}")
                        print(f"  - Role: {player_data.get('role', 'Unknown')}")
                        
                        # Show batting stats if available
                        if 'batting' in player_data:
                            batting = player_data['batting']
                            print(f"  - Batting Average: {batting.get('average', 'N/A')}")
                            print(f"  - Strike Rate: {batting.get('strikeRate', 'N/A')}")
                        
                        # Show bowling stats if available
                        if 'bowling' in player_data:
                            bowling = player_data['bowling']
                            print(f"  - Bowling Average: {bowling.get('average', 'N/A')}")
                            print(f"  - Economy Rate: {bowling.get('economyRate', 'N/A')}")
                    
                    return True
                else:
                    print(f"❌ Stats Error: {stats_response.status_code}")
                    print(f"Response: {stats_response.text}")
            else:
                print("❌ No players found in search")
        else:
            print(f"❌ Search Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Player Stats Error: {e}")
        return False
    
    return False

def main():
    """Main test function"""
    print("🏏 CricAPI Integration Test")
    print("=" * 50)
    
    # Test basic connection
    if test_cricapi_connection():
        print("\n✅ Basic API connection successful!")
    else:
        print("\n❌ Basic API connection failed!")
        return
    
    # Test player statistics
    if test_player_stats():
        print("\n✅ Player statistics retrieval successful!")
    else:
        print("\n❌ Player statistics retrieval failed!")
    
    print("\n" + "=" * 50)
    print("🎯 CricAPI Integration Test Complete!")
    print("\nNext steps:")
    print("1. Copy env_template to .env")
    print("2. Add your language model API key (OpenAI or Gemini)")
    print("3. Run: python app/main.py")

if __name__ == "__main__":
    main()
