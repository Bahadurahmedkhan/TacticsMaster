"""
Unit tests for the Tactics Master Agent

This module contains tests for the core agent functionality.
"""

import unittest
from unittest.mock import Mock, patch
import json
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from agent import TacticsMasterAgent
from tools.cricket_api_tools import get_player_stats, get_team_squad
from tools.tactical_tools import analyze_weaknesses, find_best_matchup

class TestTacticsMasterAgent(unittest.TestCase):
    """Test cases for the TacticsMasterAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_llm = Mock()
        self.mock_tools = [Mock(), Mock()]
        self.agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.llm, self.mock_llm)
        self.assertEqual(self.agent.tools, self.mock_tools)
        self.assertIsNone(self.agent.agent_executor)
    
    def test_create_agent_prompt(self):
        """Test agent prompt creation"""
        prompt = self.agent.create_agent_prompt()
        self.assertIsNotNone(prompt)
        self.assertIn("Tactics Master", str(prompt))
    
    def test_get_available_tools(self):
        """Test getting available tools"""
        self.mock_tools[0].name = "tool1"
        self.mock_tools[1].name = "tool2"
        
        tools = self.agent.get_available_tools()
        self.assertEqual(tools, ["tool1", "tool2"])
    
    def test_get_agent_info(self):
        """Test getting agent information"""
        info = self.agent.get_agent_info()
        
        self.assertEqual(info["name"], "Tactics Master")
        self.assertEqual(info["version"], "1.0.0")
        self.assertIn("cricket", info["description"].lower())

class TestCricketApiTools(unittest.TestCase):
    """Test cases for cricket API tools"""
    
    def test_get_player_stats(self):
        """Test get_player_stats tool"""
        result = get_player_stats("Virat Kohli")
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Virat Kohli")
    
    def test_get_team_squad(self):
        """Test get_team_squad tool"""
        result = get_team_squad("India")
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("team_name", data)
        self.assertEqual(data["team_name"], "India")
    
    def test_get_player_stats_error_handling(self):
        """Test error handling in get_player_stats"""
        # Test with invalid input
        result = get_player_stats("")
        
        # Should return error JSON
        data = json.loads(result)
        self.assertIn("error", data)

class TestTacticalTools(unittest.TestCase):
    """Test cases for tactical analysis tools"""
    
    def test_analyze_weaknesses(self):
        """Test analyze_weaknesses tool"""
        # Create mock player data
        player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {
                "against_spin": {"average": 25.0}
            }
        }
        
        result = analyze_weaknesses(json.dumps(player_data))
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Test Player")
    
    def test_find_best_matchup(self):
        """Test find_best_matchup tool"""
        # Create mock player data
        player1_data = {
            "player_name": "Player 1",
            "recent_form": {"batting_average": 50.0}
        }
        player2_data = {
            "player_name": "Player 2", 
            "recent_form": {"batting_average": 40.0}
        }
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player1", data)
        self.assertIn("player2", data)
    
    def test_analyze_weaknesses_invalid_data(self):
        """Test analyze_weaknesses with invalid data"""
        result = analyze_weaknesses("invalid json")
        
        # Should return error JSON
        data = json.loads(result)
        self.assertIn("error", data)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    @patch('app.tools.cricket_api_tools.os.getenv')
    def test_tool_integration(self, mock_getenv):
        """Test integration between tools"""
        mock_getenv.return_value = "test_key"
        
        # Test the complete workflow
        player_stats = get_player_stats("Virat Kohli")
        analysis = analyze_weaknesses(player_stats)
        
        # Both should return valid JSON
        self.assertIsInstance(player_stats, str)
        self.assertIsInstance(analysis, str)
        
        # Should be able to parse both
        json.loads(player_stats)
        json.loads(analysis)

if __name__ == '__main__':
    unittest.main()
