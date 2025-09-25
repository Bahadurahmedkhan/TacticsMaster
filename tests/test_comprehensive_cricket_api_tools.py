"""
Comprehensive Unit Tests for Cricket API Tools

This module contains comprehensive unit tests for all cricket API tools including
get_player_stats, get_team_squad, get_matchup_data, and get_venue_stats with
extensive error handling and mock data scenarios.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
import requests
from typing import Dict, Any, Optional

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.cricket_api_tools import (
    get_player_stats,
    get_team_squad,
    get_matchup_data,
    get_venue_stats,
    _fetch_real_player_data,
    _fetch_from_cricapi,
    _fetch_from_espn_cricket,
    _fetch_from_sportmonks,
    _format_cricapi_data,
    _format_espn_data,
    _format_sportmonks_data
)

class TestCricketApiToolsComprehensive(unittest.TestCase):
    """Comprehensive test cases for cricket API tools"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_player_name = "Virat Kohli"
        self.sample_team_name = "India"
        self.sample_venue_name = "Narendra Modi Stadium"
        
        # Sample mock data structures
        self.sample_player_data = {
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
                }
            },
            "strengths": {
                "against_pace": {
                    "average": 48.9,
                    "strike_rate": 132.1
                }
            }
        }
    
    def test_get_player_stats_success(self):
        """Test successful player stats retrieval"""
        result = get_player_stats(self.sample_player_name)
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], self.sample_player_name)
        self.assertIn("recent_form", data)
        self.assertIn("weaknesses", data)
        self.assertIn("strengths", data)
    
    def test_get_player_stats_empty_name(self):
        """Test player stats with empty name"""
        result = get_player_stats("")
        
        data = json.loads(result)
        self.assertIn("error", data)
        self.assertEqual(data["player_name"], "")
    
    def test_get_player_stats_none_name(self):
        """Test player stats with None name"""
        result = get_player_stats(None)
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_get_player_stats_whitespace_name(self):
        """Test player stats with whitespace-only name"""
        result = get_player_stats("   ")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_get_player_stats_special_characters(self):
        """Test player stats with special characters in name"""
        special_name = "Virat Kohli!@#$%^&*()"
        result = get_player_stats(special_name)
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], special_name)
        self.assertIn("recent_form", data)
    
    def test_get_player_stats_unicode_name(self):
        """Test player stats with unicode characters"""
        unicode_name = "Virat Kohli 你好"
        result = get_player_stats(unicode_name)
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], unicode_name)
        self.assertIn("recent_form", data)
    
    def test_get_player_stats_very_long_name(self):
        """Test player stats with very long name"""
        long_name = "A" * 1000
        result = get_player_stats(long_name)
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], long_name)
        self.assertIn("recent_form", data)
    
    @patch('app.tools.cricket_api_tools._fetch_real_player_data')
    def test_get_player_stats_with_real_data(self, mock_fetch_real):
        """Test player stats with real API data"""
        # Mock real data response
        mock_real_data = {
            "player_name": "Virat Kohli",
            "source": "CricAPI",
            "recent_form": {
                "batting_average": 50.0,
                "strike_rate": 120.0
            }
        }
        mock_fetch_real.return_value = mock_real_data
        
        result = get_player_stats(self.sample_player_name)
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Virat Kohli")
        self.assertEqual(data["source"], "CricAPI")
        mock_fetch_real.assert_called_once_with(self.sample_player_name)
    
    @patch('app.tools.cricket_api_tools._fetch_real_player_data')
    def test_get_player_stats_fallback_to_mock(self, mock_fetch_real):
        """Test player stats fallback to mock data when real data unavailable"""
        mock_fetch_real.return_value = None
        
        result = get_player_stats(self.sample_player_name)
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], self.sample_player_name)
        self.assertIn("recent_form", data)
        self.assertIn("weaknesses", data)
        self.assertIn("strengths", data)
    
    def test_get_team_squad_success(self):
        """Test successful team squad retrieval"""
        result = get_team_squad(self.sample_team_name)
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("team_name", data)
        self.assertEqual(data["team_name"], self.sample_team_name)
        self.assertIn("squad", data)
        self.assertIn("recent_performance", data)
        self.assertIn("strengths", data)
        self.assertIn("weaknesses", data)
        self.assertIn("key_players", data)
    
    def test_get_team_squad_empty_name(self):
        """Test team squad with empty name"""
        result = get_team_squad("")
        
        data = json.loads(result)
        self.assertEqual(data["team_name"], "")
        self.assertIn("squad", data)
    
    def test_get_team_squad_none_name(self):
        """Test team squad with None name"""
        result = get_team_squad(None)
        
        data = json.loads(result)
        self.assertIsNone(data["team_name"])
        self.assertIn("squad", data)
    
    def test_get_team_squad_special_characters(self):
        """Test team squad with special characters"""
        special_team = "India!@#$%^&*()"
        result = get_team_squad(special_team)
        
        data = json.loads(result)
        self.assertEqual(data["team_name"], special_team)
        self.assertIn("squad", data)
    
    def test_get_team_squad_unicode_name(self):
        """Test team squad with unicode characters"""
        unicode_team = "India 印度"
        result = get_team_squad(unicode_team)
        
        data = json.loads(result)
        self.assertEqual(data["team_name"], unicode_team)
        self.assertIn("squad", data)
    
    def test_get_matchup_data_success(self):
        """Test successful matchup data retrieval"""
        result = get_matchup_data("India", "Australia")
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
        self.assertIn("venue_analysis", data)
        self.assertIn("key_trends", data)
    
    def test_get_matchup_data_same_teams(self):
        """Test matchup data with same teams"""
        result = get_matchup_data("India", "India")
        
        data = json.loads(result)
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
    
    def test_get_matchup_data_empty_team_names(self):
        """Test matchup data with empty team names"""
        result = get_matchup_data("", "")
        
        data = json.loads(result)
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
    
    def test_get_matchup_data_none_team_names(self):
        """Test matchup data with None team names"""
        result = get_matchup_data(None, None)
        
        data = json.loads(result)
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
    
    def test_get_matchup_data_special_characters(self):
        """Test matchup data with special characters"""
        result = get_matchup_data("India!@#", "Australia$%^")
        
        data = json.loads(result)
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
    
    def test_get_venue_stats_success(self):
        """Test successful venue stats retrieval"""
        result = get_venue_stats(self.sample_venue_name)
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("venue_name", data)
        self.assertEqual(data["venue_name"], self.sample_venue_name)
        self.assertIn("pitch_conditions", data)
        self.assertIn("average_scores", data)
        self.assertIn("weather_impact", data)
        self.assertIn("venue_records", data)
        self.assertIn("home_advantage", data)
    
    def test_get_venue_stats_empty_name(self):
        """Test venue stats with empty name"""
        result = get_venue_stats("")
        
        data = json.loads(result)
        self.assertEqual(data["venue_name"], "")
        self.assertIn("pitch_conditions", data)
    
    def test_get_venue_stats_none_name(self):
        """Test venue stats with None name"""
        result = get_venue_stats(None)
        
        data = json.loads(result)
        self.assertIsNone(data["venue_name"])
        self.assertIn("pitch_conditions", data)
    
    def test_get_venue_stats_special_characters(self):
        """Test venue stats with special characters"""
        special_venue = "Narendra Modi Stadium!@#$%^&*()"
        result = get_venue_stats(special_venue)
        
        data = json.loads(result)
        self.assertEqual(data["venue_name"], special_venue)
        self.assertIn("pitch_conditions", data)
    
    def test_get_venue_stats_unicode_name(self):
        """Test venue stats with unicode characters"""
        unicode_venue = "Narendra Modi Stadium 纳伦德拉·莫迪体育场"
        result = get_venue_stats(unicode_venue)
        
        data = json.loads(result)
        self.assertEqual(data["venue_name"], unicode_venue)
        self.assertIn("pitch_conditions", data)

class TestCricketApiToolsErrorHandling(unittest.TestCase):
    """Test error handling scenarios for cricket API tools"""
    
    def test_get_player_stats_exception_handling(self):
        """Test exception handling in get_player_stats"""
        # This test ensures the function handles exceptions gracefully
        # by returning error JSON instead of crashing
        result = get_player_stats("Test Player")
        
        # Should not raise exception
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIsNotNone(data)
    
    def test_get_team_squad_exception_handling(self):
        """Test exception handling in get_team_squad"""
        result = get_team_squad("Test Team")
        
        # Should not raise exception
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIsNotNone(data)
    
    def test_get_matchup_data_exception_handling(self):
        """Test exception handling in get_matchup_data"""
        result = get_matchup_data("Team1", "Team2")
        
        # Should not raise exception
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIsNotNone(data)
    
    def test_get_venue_stats_exception_handling(self):
        """Test exception handling in get_venue_stats"""
        result = get_venue_stats("Test Venue")
        
        # Should not raise exception
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIsNotNone(data)

class TestRealApiIntegration(unittest.TestCase):
    """Test real API integration functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_player_name = "Virat Kohli"
    
    @patch('app.tools.cricket_api_tools.CRICAPI_KEY', 'test_key')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_real_player_data_with_cricapi(self, mock_get):
        """Test fetching real player data from CricAPI"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": [{"id": "123", "name": "Virat Kohli"}]
        }
        mock_get.return_value = mock_response
        
        result = _fetch_real_player_data(self.sample_player_name)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "CricAPI")
    
    @patch('app.tools.cricket_api_tools.CRICAPI_KEY', '')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_real_player_data_no_api_key(self, mock_get):
        """Test fetching real player data without API key"""
        result = _fetch_real_player_data(self.sample_player_name)
        
        self.assertIsNone(result)
        mock_get.assert_not_called()
    
    @patch('app.tools.cricket_api_tools.CRICAPI_KEY', 'test_key')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_cricapi_success(self, mock_get):
        """Test successful CricAPI fetch"""
        # Mock search response
        search_response = Mock()
        search_response.status_code = 200
        search_response.json.return_value = {
            "status": "success",
            "data": [{"id": "123", "name": "Virat Kohli"}]
        }
        
        # Mock stats response
        stats_response = Mock()
        stats_response.status_code = 200
        stats_response.json.return_value = {
            "batting_average": 50.0,
            "strike_rate": 120.0
        }
        
        mock_get.side_effect = [search_response, stats_response]
        
        result = _fetch_from_cricapi(self.sample_player_name)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "CricAPI")
    
    @patch('app.tools.cricket_api_tools.CRICAPI_KEY', 'test_key')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_cricapi_failure(self, mock_get):
        """Test CricAPI fetch failure"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = _fetch_from_cricapi(self.sample_player_name)
        
        self.assertIsNone(result)
    
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_espn_cricket_success(self, mock_get):
        """Test successful ESPN Cricket fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"players": []}
        mock_get.return_value = mock_response
        
        result = _fetch_from_espn_cricket(self.sample_player_name)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "ESPN Cricket")
    
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_espn_cricket_failure(self, mock_get):
        """Test ESPN Cricket fetch failure"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = _fetch_from_espn_cricket(self.sample_player_name)
        
        self.assertIsNone(result)
    
    @patch('app.tools.cricket_api_tools.CRICKET_API_KEY', 'test_key')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_sportmonks_success(self, mock_get):
        """Test successful Sportmonks fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        result = _fetch_from_sportmonks(self.sample_player_name)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "Sportmonks")
    
    @patch('app.tools.cricket_api_tools.CRICKET_API_KEY', 'test_key')
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_fetch_from_sportmonks_failure(self, mock_get):
        """Test Sportmonks fetch failure"""
        mock_response = Mock()
        mock_response.status_code = 401  # Unauthorized
        mock_get.return_value = mock_response
        
        result = _fetch_from_sportmonks(self.sample_player_name)
        
        self.assertIsNone(result)
    
    def test_format_cricapi_data(self):
        """Test CricAPI data formatting"""
        raw_data = {
            "batting_average": 50.0,
            "strike_rate": 120.0,
            "bowling_average": 25.0,
            "economy_rate": 4.5,
            "career_stats": {"matches": 100},
            "recent_matches": [{"runs": 50}]
        }
        
        result = _format_cricapi_data(raw_data, self.sample_player_name)
        
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "CricAPI")
        self.assertEqual(result["recent_form"]["batting_average"], 50.0)
        self.assertEqual(result["recent_form"]["strike_rate"], 120.0)
        self.assertIn("career_stats", result)
        self.assertIn("recent_matches", result)
    
    def test_format_espn_data(self):
        """Test ESPN data formatting"""
        raw_data = {"players": []}
        
        result = _format_espn_data(raw_data, self.sample_player_name)
        
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "ESPN Cricket")
        self.assertIn("api_data", result)
    
    def test_format_sportmonks_data(self):
        """Test Sportmonks data formatting"""
        raw_data = {"data": []}
        
        result = _format_sportmonks_data(raw_data, self.sample_player_name)
        
        self.assertEqual(result["player_name"], self.sample_player_name)
        self.assertEqual(result["source"], "Sportmonks")
        self.assertIn("api_data", result)

class TestCricketApiToolsDataValidation(unittest.TestCase):
    """Test data validation and structure for cricket API tools"""
    
    def test_player_stats_data_structure(self):
        """Test player stats data structure"""
        result = get_player_stats("Virat Kohli")
        data = json.loads(result)
        
        # Check required fields exist
        required_fields = ["player_name", "recent_form", "weaknesses", "strengths"]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data["recent_form"], dict)
        self.assertIsInstance(data["weaknesses"], dict)
        self.assertIsInstance(data["strengths"], dict)
        
        # Check recent_form structure
        recent_form = data["recent_form"]
        self.assertIn("batting_average", recent_form)
        self.assertIn("strike_rate", recent_form)
        self.assertIsInstance(recent_form["batting_average"], (int, float))
        self.assertIsInstance(recent_form["strike_rate"], (int, float))
    
    def test_team_squad_data_structure(self):
        """Test team squad data structure"""
        result = get_team_squad("India")
        data = json.loads(result)
        
        # Check required fields exist
        required_fields = ["team_name", "squad", "recent_performance", "strengths", "weaknesses", "key_players"]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data["squad"], dict)
        self.assertIsInstance(data["recent_performance"], dict)
        self.assertIsInstance(data["strengths"], list)
        self.assertIsInstance(data["weaknesses"], list)
        self.assertIsInstance(data["key_players"], dict)
        
        # Check squad structure
        squad = data["squad"]
        self.assertIn("batsmen", squad)
        self.assertIn("bowlers", squad)
        self.assertIn("all_rounders", squad)
        self.assertIsInstance(squad["batsmen"], list)
        self.assertIsInstance(squad["bowlers"], list)
        self.assertIsInstance(squad["all_rounders"], list)
    
    def test_matchup_data_data_structure(self):
        """Test matchup data structure"""
        result = get_matchup_data("India", "Australia")
        data = json.loads(result)
        
        # Check required fields exist
        required_fields = ["head_to_head", "recent_encounters", "venue_analysis", "key_trends"]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data["head_to_head"], dict)
        self.assertIsInstance(data["recent_encounters"], list)
        self.assertIsInstance(data["venue_analysis"], dict)
        self.assertIsInstance(data["key_trends"], list)
        
        # Check head_to_head structure
        head_to_head = data["head_to_head"]
        self.assertIn("total_matches", head_to_head)
        self.assertIn("team1_wins", head_to_head)
        self.assertIn("team2_wins", head_to_head)
        self.assertIn("win_percentage", head_to_head)
    
    def test_venue_stats_data_structure(self):
        """Test venue stats data structure"""
        result = get_venue_stats("Narendra Modi Stadium")
        data = json.loads(result)
        
        # Check required fields exist
        required_fields = ["venue_name", "pitch_conditions", "average_scores", "weather_impact", "venue_records", "home_advantage"]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data["pitch_conditions"], dict)
        self.assertIsInstance(data["average_scores"], dict)
        self.assertIsInstance(data["weather_impact"], dict)
        self.assertIsInstance(data["venue_records"], dict)
        self.assertIsInstance(data["home_advantage"], dict)
        
        # Check pitch_conditions structure
        pitch_conditions = data["pitch_conditions"]
        self.assertIn("type", pitch_conditions)
        self.assertIn("pace_friendly", pitch_conditions)
        self.assertIn("spin_friendly", pitch_conditions)
        self.assertIn("bounce", pitch_conditions)

if __name__ == '__main__':
    unittest.main()
