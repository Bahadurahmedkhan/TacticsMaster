import httpx
import os
from typing import Dict, List, Any, Optional
import json

class CricketDataTool:
    """
    Tool for fetching cricket data from external APIs
    """
    
    def __init__(self):
        self.api_key = os.getenv("CRICKET_API_KEY")
        self.base_url = os.getenv("CRICKET_API_BASE_URL", "https://api.sportmonks.com/v3/football")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_data(self, query: str) -> str:
        """
        Fetch cricket data based on the query
        
        Args:
            query: The data request (e.g., "Get stats for Virat Kohli")
            
        Returns:
            JSON string containing the requested data
        """
        try:
            # Parse the query to determine what data to fetch
            data_type = self._parse_query(query)
            
            if data_type == "player_stats":
                return await self._get_player_stats(query)
            elif data_type == "team_info":
                return await self._get_team_info(query)
            elif data_type == "match_history":
                return await self._get_match_history(query)
            else:
                return await self._get_general_data(query)
                
        except Exception as e:
            return json.dumps({
                "error": f"Failed to fetch cricket data: {str(e)}",
                "data": {}
            })
    
    def _parse_query(self, query: str) -> str:
        """Parse the query to determine data type"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["player", "batsman", "bowler", "stats"]):
            return "player_stats"
        elif any(word in query_lower for word in ["team", "squad", "roster"]):
            return "team_info"
        elif any(word in query_lower for word in ["match", "game", "history", "previous"]):
            return "match_history"
        else:
            return "general"
    
    async def _get_player_stats(self, query: str) -> str:
        """Get player statistics"""
        # Mock data for demonstration - replace with actual API calls
        mock_data = {
            "player_name": "Virat Kohli",
            "recent_form": {
                "last_10_innings": [45, 67, 23, 89, 12, 78, 34, 56, 91, 43],
                "average": 54.8,
                "strike_rate": 125.6
            },
            "weaknesses": {
                "against_spin": {
                    "average": 28.4,
                    "strike_rate": 95.2,
                    "dismissal_rate": 0.15
                },
                "early_innings": {
                    "first_10_balls": {
                        "average": 18.7,
                        "strike_rate": 78.3
                    }
                }
            },
            "strengths": {
                "death_overs": {
                    "overs_16_20": {
                        "average": 42.3,
                        "strike_rate": 145.8
                    }
                },
                "against_pace": {
                    "average": 48.9,
                    "strike_rate": 132.1
                }
            },
            "recent_matches": [
                {
                    "opponent": "Australia",
                    "runs": 89,
                    "balls": 67,
                    "strike_rate": 132.8,
                    "result": "Won"
                },
                {
                    "opponent": "England",
                    "runs": 34,
                    "balls": 28,
                    "strike_rate": 121.4,
                    "result": "Lost"
                }
            ]
        }
        
        return json.dumps(mock_data, indent=2)
    
    async def _get_team_info(self, query: str) -> str:
        """Get team information"""
        mock_data = {
            "team_name": "India",
            "squad": {
                "batsmen": ["Rohit Sharma", "Virat Kohli", "KL Rahul", "Suryakumar Yadav"],
                "bowlers": ["Jasprit Bumrah", "Mohammed Shami", "Ravindra Jadeja", "Kuldeep Yadav"],
                "all_rounders": ["Hardik Pandya", "Ravindra Jadeja", "Axar Patel"]
            },
            "recent_performance": {
                "last_5_matches": ["W", "L", "W", "W", "L"],
                "win_percentage": 60
            },
            "strengths": [
                "Strong batting lineup",
                "Quality spin bowling",
                "Good fielding unit"
            ],
            "weaknesses": [
                "Inconsistent middle order",
                "Death bowling concerns",
                "Over-reliance on top order"
            ]
        }
        
        return json.dumps(mock_data, indent=2)
    
    async def _get_match_history(self, query: str) -> str:
        """Get match history and head-to-head data"""
        mock_data = {
            "head_to_head": {
                "total_matches": 45,
                "india_wins": 28,
                "opponent_wins": 17,
                "win_percentage": 62.2
            },
            "recent_encounters": [
                {
                    "date": "2023-11-19",
                    "venue": "Narendra Modi Stadium",
                    "result": "India won by 6 wickets",
                    "key_performers": ["Virat Kohli: 89*", "Jasprit Bumrah: 3/18"]
                },
                {
                    "date": "2023-10-08",
                    "venue": "Melbourne Cricket Ground",
                    "result": "Opponent won by 4 wickets",
                    "key_performers": ["Opponent Captain: 78", "Opponent Bowler: 4/25"]
                }
            ],
            "venue_analysis": {
                "narendra_modi_stadium": {
                    "matches_played": 8,
                    "india_wins": 6,
                    "average_score": 285,
                    "pitch_type": "Batting friendly"
                }
            }
        }
        
        return json.dumps(mock_data, indent=2)
    
    async def _get_general_data(self, query: str) -> str:
        """Get general cricket data"""
        mock_data = {
            "query": query,
            "data": {
                "message": "General cricket data requested",
                "available_data_types": [
                    "Player statistics",
                    "Team information", 
                    "Match history",
                    "Venue analysis",
                    "Head-to-head records"
                ]
            }
        }
        
        return json.dumps(mock_data, indent=2)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
