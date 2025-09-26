"""
Pytest configuration and fixtures for Tactics Master testing

This module provides shared fixtures and configuration for all test modules.
It includes common test data, mock objects, and utility functions.
"""

import pytest
import json
import os
import sys
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any, List, Optional
import asyncio
from fastapi.testclient import TestClient

# Add project paths to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import project modules
from app.agent import TacticsMasterAgent
from app.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ConfigurationError,
    ValidationError,
    APIConnectionError,
    APITimeoutError,
    CricketDataError,
    APIResponseError,
    DataValidationError,
    ServiceUnavailableError
)

# Test configuration
TEST_CONFIG = {
    "test_api_key": "test_key_12345",
    "test_gemini_key": "test_gemini_12345",
    "test_cricket_key": "test_cricket_12345",
    "test_openai_key": "test_openai_12345"
}

@pytest.fixture
def mock_llm():
    """Mock language model for testing"""
    mock = Mock()
    mock.model_name = "test-model"
    mock.invoke = Mock(return_value=Mock(content="Test response"))
    return mock

@pytest.fixture
def mock_tools():
    """Mock tools for testing"""
    tools = []
    for i in range(4):
        tool = Mock()
        tool.name = f"test_tool_{i}"
        tool.description = f"Test tool {i} description"
        tools.append(tool)
    return tools

@pytest.fixture
def sample_player_data():
    """Sample player data for testing"""
    return {
        "player_name": "Virat Kohli",
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

@pytest.fixture
def sample_team_data():
    """Sample team data for testing"""
    return {
        "team_name": "India",
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

@pytest.fixture
def sample_matchup_data():
    """Sample matchup data for testing"""
    return {
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
                "result": "India won by 6 wickets",
                "key_performers": ["Virat Kohli: 89*", "Jasprit Bumrah: 3/18"]
            },
            {
                "date": "2023-10-08",
                "venue": "Melbourne Cricket Ground",
                "result": "Australia won by 4 wickets",
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
            "Strong recent form for India",
            "Australia struggles in subcontinent conditions",
            "Close contests in recent matches"
        ]
    }

@pytest.fixture
def sample_venue_data():
    """Sample venue data for testing"""
    return {
        "venue_name": "Narendra Modi Stadium",
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

@pytest.fixture
def sample_analysis_response():
    """Sample analysis response for testing"""
    return {
        "response": "Comprehensive analysis of Virat Kohli's batting weaknesses",
        "analysis": {
            "player_name": "Virat Kohli",
            "weaknesses": ["against_spin", "early_innings"],
            "recommendations": ["Use spin bowling", "Attack early"]
        },
        "sources": ["CricAPI", "Historical Data", "Tactical Analysis"]
    }

@pytest.fixture
def sample_query_request():
    """Sample query request for testing"""
    return {
        "query": "Analyze Virat Kohli's batting weaknesses against Australia",
        "context": {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium"
        }
    }

@pytest.fixture
def mock_agent():
    """Mock agent for testing"""
    mock = Mock()
    mock.analyze = Mock(return_value={
        "response": "Test analysis response",
        "analysis": {"player_name": "Virat Kohli"},
        "sources": ["CricAPI"]
    })
    return mock

@pytest.fixture
def test_client():
    """Test client for FastAPI testing"""
    # Mock the hybrid_agent import
    with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
        from backend.main import app
        return TestClient(app)

@pytest.fixture
def mock_requests():
    """Mock requests for API testing"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": []}
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_environment():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': TEST_CONFIG['test_openai_key'],
        'GEMINI_API_KEY': TEST_CONFIG['test_gemini_key'],
        'CRICKET_API_KEY': TEST_CONFIG['test_cricket_key'],
        'CRICAPI_KEY': TEST_CONFIG['test_api_key']
    }):
        yield

@pytest.fixture
def mock_async_agent():
    """Mock async agent for testing"""
    mock = Mock()
    mock.analyze = Mock(return_value=asyncio.create_task(
        asyncio.coroutine(lambda: {
            "response": "Test async analysis response",
            "analysis": {"player_name": "Virat Kohli"},
            "sources": ["CricAPI"]
        })()
    ))
    return mock

# Test utilities
class TestUtils:
    """Utility functions for testing"""
    
    @staticmethod
    def create_mock_llm(model_name: str = "test-model"):
        """Create a mock LLM with specified model name"""
        mock = Mock()
        mock.model_name = model_name
        mock.invoke = Mock(return_value=Mock(content="Test response"))
        return mock
    
    @staticmethod
    def create_mock_tool(name: str, description: str = "Test tool"):
        """Create a mock tool with specified name and description"""
        tool = Mock()
        tool.name = name
        tool.description = description
        return tool
    
    @staticmethod
    def create_sample_context():
        """Create sample context for testing"""
        return {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "ODI"
        }
    
    @staticmethod
    def create_error_response(error_type: str, message: str):
        """Create error response for testing"""
        return {
            "error": message,
            "error_type": error_type,
            "success": False
        }
    
    @staticmethod
    def validate_json_response(response: str) -> bool:
        """Validate that response is valid JSON"""
        try:
            json.loads(response)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def create_large_test_data(size: int = 1000):
        """Create large test data for performance testing"""
        return {
            "data": {f"key_{i}": f"value_{i}" for i in range(size)},
            "players": [f"Player {i}" for i in range(size)],
            "matches": [{"id": i, "score": i * 10} for i in range(size)]
        }

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as requiring API access"
    )

# Test data generators
class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def generate_player_names(count: int = 10) -> List[str]:
        """Generate list of player names for testing"""
        return [f"Player {i}" for i in range(count)]
    
    @staticmethod
    def generate_team_names(count: int = 5) -> List[str]:
        """Generate list of team names for testing"""
        teams = ["India", "Australia", "England", "South Africa", "New Zealand"]
        return teams[:count]
    
    @staticmethod
    def generate_venue_names(count: int = 5) -> List[str]:
        """Generate list of venue names for testing"""
        venues = [
            "Narendra Modi Stadium",
            "Melbourne Cricket Ground",
            "Lord's Cricket Ground",
            "Newlands Cricket Ground",
            "Eden Park"
        ]
        return venues[:count]
    
    @staticmethod
    def generate_match_scenarios(count: int = 5) -> List[Dict[str, Any]]:
        """Generate match scenarios for testing"""
        scenarios = []
        for i in range(count):
            scenarios.append({
                "team1": f"Team {i*2}",
                "team2": f"Team {i*2+1}",
                "venue": f"Venue {i}",
                "match_type": ["ODI", "T20", "Test"][i % 3]
            })
        return scenarios

# Performance testing utilities
class PerformanceTestUtils:
    """Utilities for performance testing"""
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """Measure execution time of a function"""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    
    @staticmethod
    def create_memory_intensive_data(size_mb: int = 10):
        """Create memory intensive test data"""
        import sys
        target_size = size_mb * 1024 * 1024  # Convert MB to bytes
        data = []
        current_size = 0
        
        while current_size < target_size:
            chunk = "x" * 1024  # 1KB chunk
            data.append(chunk)
            current_size += sys.getsizeof(chunk)
        
        return data
