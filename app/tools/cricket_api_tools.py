"""
Cricket API Tools for Tactics Master Agent

This module contains LangChain tools for interacting with external cricket data APIs.
Each tool is decorated with @tool and provides specific functionality for fetching
cricket-related data including player statistics, team information, and match data.

Author: Tactics Master Team
Version: 1.0.0
"""

# Standard library imports
import os
import json
import logging
from typing import Dict, Any, Optional

# Third-party imports
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

# Local imports
from exceptions import (
    CricketDataError,
    APIConnectionError,
    APITimeoutError,
    APIResponseError,
    DataValidationError,
    ServiceUnavailableError
)

# Configure logging
logger = logging.getLogger(__name__)

# API Configuration
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY", "")
CRICKET_API_BASE_URL = os.getenv("CRICKET_API_BASE_URL", "https://api.sportmonks.com/v3/football")
CRICAPI_KEY = os.getenv("CRICAPI_KEY", "")
ESPN_CRICKET_API_KEY = os.getenv("ESPN_CRICKET_API_KEY", "")

# API Endpoints
SPORTMONKS_BASE = "https://api.sportmonks.com/v3/football"
CRICAPI_BASE = "https://api.cricapi.com/v1"
ESPN_CRICKET_BASE = "https://site.api.espn.com/apis/site/v2/sports/cricket"

class PlayerStatsInput(BaseModel):
    """Input schema for get_player_stats tool"""
    player_name: str = Field(description="Name of the player to get stats for")

class TeamSquadInput(BaseModel):
    """Input schema for get_team_squad tool"""
    team_name: str = Field(description="Name of the team to get squad for")

class MatchupDataInput(BaseModel):
    """Input schema for get_matchup_data tool"""
    team1: str = Field(description="First team name")
    team2: str = Field(description="Second team name")

class VenueStatsInput(BaseModel):
    """Input schema for get_venue_stats tool"""
    venue_name: str = Field(description="Name of the venue to get stats for")

@tool(args_schema=PlayerStatsInput)
def get_player_stats(player_name: str) -> str:
    """
    Fetch detailed player statistics and recent form.
    
    This tool retrieves comprehensive player data including:
    - Recent batting/bowling averages
    - Strike rates and economy rates
    - Performance against different bowling types
    - Recent match performances
    - Weaknesses and strengths analysis
    
    Args:
        player_name: Name of the player to analyze
        
    Returns:
        str: JSON string containing player statistics and analysis
        
    Raises:
        Exception: If data fetching fails
    """
    if not player_name or not player_name.strip():
        logger.warning("Empty player name provided")
        raise DataValidationError(
            message="Player name cannot be empty",
            error_code="EMPTY_PLAYER_NAME",
            context={"player_name": player_name}
        )
    
    try:
        logger.info(f"Fetching player stats for: {player_name}")
        
        # Try to fetch real data from APIs first
        real_data = _fetch_real_player_data(player_name)
        if real_data:
            logger.info(f"Successfully fetched real data for {player_name}")
            return json.dumps(real_data, indent=2)
        
        # Fallback to mock data for demonstration
        mock_data = {
            "player_name": player_name,
            "recent_form": {
                "last_10_innings": [45, 67, 23, 89, 12, 78, 34, 56, 91, 43],
                "batting_average": 54.8,
                "strike_rate": 125.6,
                "bowling_average": 28.4,
                "economy_rate": 5.2
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
        
        logger.info(f"Using mock data for {player_name}")
        return json.dumps(mock_data, indent=2)
        
    except DataValidationError:
        # Re-raise validation errors
        raise
    except requests.ConnectionError as e:
        logger.error(f"Connection error fetching player stats for {player_name}: {e}")
        raise APIConnectionError(
            message=f"Failed to connect to cricket data API: {str(e)}",
            error_code="API_CONNECTION_ERROR",
            context={"player_name": player_name, "original_error": str(e)}
        )
    except requests.Timeout as e:
        logger.error(f"Timeout fetching player stats for {player_name}: {e}")
        raise APITimeoutError(
            message=f"Cricket data API request timed out: {str(e)}",
            error_code="API_TIMEOUT_ERROR",
            context={"player_name": player_name, "original_error": str(e)}
        )
    except requests.HTTPError as e:
        logger.error(f"HTTP error fetching player stats for {player_name}: {e}")
        raise APIResponseError(
            message=f"Cricket data API returned error: {str(e)}",
            error_code="API_HTTP_ERROR",
            context={"player_name": player_name, "status_code": e.response.status_code if e.response else None}
        )
    except Exception as e:
        logger.error(f"Failed to fetch player stats for {player_name}: {e}")
        raise CricketDataError(
            message=f"Failed to fetch player stats: {str(e)}",
            error_code="PLAYER_STATS_ERROR",
            context={"player_name": player_name, "original_error": str(e)}
        )

@tool(args_schema=TeamSquadInput)
def get_team_squad(team_name: str) -> str:
    """
    Get team squad information and player roles.
    
    This tool retrieves comprehensive team data including:
    - Squad composition (batsmen, bowlers, all-rounders)
    - Player roles and specializations
    - Recent team performance
    - Team strengths and weaknesses
    - Key players and their importance
    
    Args:
        team_name: Name of the team to analyze
        
    Returns:
        str: JSON string containing team squad information
    """
    try:
        # Mock data for demonstration - replace with actual API calls
        mock_data = {
            "team_name": team_name,
            "squad": {
                "batsmen": ["Rohit Sharma", "Virat Kohli", "KL Rahul", "Suryakumar Yadav"],
                "bowlers": ["Jasprit Bumrah", "Mohammed Shami", "Ravindra Jadeja", "Kuldeep Yadav"],
                "all_rounders": ["Hardik Pandya", "Ravindra Jadeja", "Axar Patel"]
            },
            "recent_performance": {
                "last_5_matches": ["W", "L", "W", "W", "L"],
                "win_percentage": 60,
                "form_rating": "Good"
            },
            "strengths": [
                "Strong batting lineup",
                "Quality spin bowling",
                "Good fielding unit",
                "Experienced leadership"
            ],
            "weaknesses": [
                "Inconsistent middle order",
                "Death bowling concerns",
                "Over-reliance on top order"
            ],
            "key_players": {
                "captain": "Rohit Sharma",
                "vice_captain": "KL Rahul",
                "star_bowler": "Jasprit Bumrah",
                "star_batsman": "Virat Kohli"
            }
        }
        
        return json.dumps(mock_data, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to fetch team squad: {str(e)}",
            "team_name": team_name
        })

@tool(args_schema=MatchupDataInput)
def get_matchup_data(team1: str, team2: str) -> str:
    """
    Retrieve head-to-head records and historical data.
    
    This tool fetches comprehensive matchup data including:
    - Head-to-head win/loss records
    - Recent encounters and results
    - Venue-specific performance
    - Key matchups and rivalries
    - Historical trends and patterns
    
    Args:
        team1: First team name
        team2: Second team name
        
    Returns:
        str: JSON string containing matchup data
    """
    try:
        # Mock data for demonstration - replace with actual API calls
        mock_data = {
            "head_to_head": {
                "total_matches": 45,
                "team1_wins": 28,
                "team2_wins": 17,
                "win_percentage": 62.2
            },
            "recent_encounters": [
                {
                    "date": "2023-11-19",
                    "venue": "Narendra Modi Stadium",
                    "result": f"{team1} won by 6 wickets",
                    "key_performers": ["Virat Kohli: 89*", "Jasprit Bumrah: 3/18"]
                },
                {
                    "date": "2023-10-08",
                    "venue": "Melbourne Cricket Ground",
                    "result": f"{team2} won by 4 wickets",
                    "key_performers": ["Opponent Captain: 78", "Opponent Bowler: 4/25"]
                }
            ],
            "venue_analysis": {
                "narendra_modi_stadium": {
                    "matches_played": 8,
                    "team1_wins": 6,
                    "average_score": 285,
                    "pitch_type": "Batting friendly"
                }
            },
            "key_trends": [
                "Strong recent form for team1",
                "Team2 struggles in subcontinent conditions",
                "Close contests in recent matches"
            ]
        }
        
        return json.dumps(mock_data, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to fetch matchup data: {str(e)}",
            "team1": team1,
            "team2": team2
        })

@tool(args_schema=VenueStatsInput)
def get_venue_stats(venue_name: str) -> str:
    """
    Get venue-specific statistics and conditions.
    
    This tool retrieves comprehensive venue data including:
    - Pitch conditions and characteristics
    - Average scores and run rates
    - Weather conditions and impact
    - Venue-specific records and trends
    - Home advantage analysis
    
    Args:
        venue_name: Name of the venue to analyze
        
    Returns:
        str: JSON string containing venue statistics
    """
    try:
        # Mock data for demonstration - replace with actual API calls
        mock_data = {
            "venue_name": venue_name,
            "pitch_conditions": {
                "type": "Batting friendly",
                "pace_friendly": True,
                "spin_friendly": False,
                "bounce": "Medium"
            },
            "average_scores": {
                "first_innings": 285,
                "second_innings": 245,
                "run_rate": 5.8
            },
            "weather_impact": {
                "dew_factor": "High",
                "wind_conditions": "Moderate",
                "temperature": "25-30°C"
            },
            "venue_records": {
                "highest_total": 398,
                "lowest_total": 78,
                "average_overs": 48.5
            },
            "home_advantage": {
                "home_team_win_percentage": 65,
                "toss_advantage": "Bat first"
            }
        }
        
        return json.dumps(mock_data, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to fetch venue stats: {str(e)}",
            "venue_name": venue_name
        })

# Real API Integration Functions

def _fetch_real_player_data(player_name: str) -> Optional[Dict[str, Any]]:
    """
    Fetch real player data from available APIs.
    
    Args:
        player_name: Name of the player
        
    Returns:
        Dict containing player data or None if not available
    """
    # Try CricAPI first (free tier available)
    if CRICAPI_KEY:
        data = _fetch_from_cricapi(player_name)
        if data:
            return data
    
    # Try ESPN Cricket API (free)
    data = _fetch_from_espn_cricket(player_name)
    if data:
        return data
    
    # Try Sportmonks if API key is available
    if CRICKET_API_KEY:
        data = _fetch_from_sportmonks(player_name)
        if data:
            return data
    
    return None

def _fetch_from_cricapi(player_name: str) -> Optional[Dict[str, Any]]:
    """Fetch player data from CricAPI"""
    try:
        # Search for player
        search_url = f"{CRICAPI_BASE}/players"
        params = {
            "apikey": CRICAPI_KEY,
            "search": player_name
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("data"):
                player_id = data["data"][0]["id"]
                
                # Get detailed player stats
                stats_url = f"{CRICAPI_BASE}/players/{player_id}"
                stats_response = requests.get(stats_url, params={"apikey": CRICAPI_KEY}, timeout=10)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    return _format_cricapi_data(stats_data, player_name)
        
        return None
    except Exception as e:
        print(f"CricAPI error: {e}")
        return None

def _fetch_from_espn_cricket(player_name: str) -> Optional[Dict[str, Any]]:
    """Fetch player data from ESPN Cricket API"""
    try:
        # ESPN Cricket API is free but has limited player search
        # This is a simplified implementation
        search_url = f"{ESPN_CRICKET_BASE}/players"
        params = {"search": player_name}
        
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return _format_espn_data(data, player_name)
        
        return None
    except Exception as e:
        print(f"ESPN Cricket API error: {e}")
        return None

def _fetch_from_sportmonks(player_name: str) -> Optional[Dict[str, Any]]:
    """Fetch player data from Sportmonks API"""
    try:
        # Sportmonks requires subscription
        search_url = f"{SPORTMONKS_BASE}/players"
        headers = {"Authorization": f"Bearer {CRICKET_API_KEY}"}
        params = {"search": player_name}
        
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return _format_sportmonks_data(data, player_name)
        
        return None
    except Exception as e:
        print(f"Sportmonks API error: {e}")
        return None

def _format_cricapi_data(data: Dict[str, Any], player_name: str) -> Dict[str, Any]:
    """Format CricAPI data into our standard format"""
    return {
        "player_name": player_name,
        "source": "CricAPI",
        "recent_form": {
            "batting_average": data.get("batting_average", 0),
            "strike_rate": data.get("strike_rate", 0),
            "bowling_average": data.get("bowling_average", 0),
            "economy_rate": data.get("economy_rate", 0)
        },
        "career_stats": data.get("career_stats", {}),
        "recent_matches": data.get("recent_matches", []),
        "api_data": data
    }

def _format_espn_data(data: Dict[str, Any], player_name: str) -> Dict[str, Any]:
    """Format ESPN Cricket data into our standard format"""
    return {
        "player_name": player_name,
        "source": "ESPN Cricket",
        "recent_form": {
            "batting_average": 0,  # ESPN doesn't provide detailed stats
            "strike_rate": 0
        },
        "api_data": data
    }

def _format_sportmonks_data(data: Dict[str, Any], player_name: str) -> Dict[str, Any]:
    """Format Sportmonks data into our standard format"""
    return {
        "player_name": player_name,
        "source": "Sportmonks",
        "recent_form": {
            "batting_average": 0,  # Format based on Sportmonks response
            "strike_rate": 0
        },
        "api_data": data
    }
