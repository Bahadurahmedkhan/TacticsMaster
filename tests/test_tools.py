"""
Unit tests for Tactics Master Tools

This module contains tests for the cricket API tools and tactical analysis tools.
"""

import unittest
import json
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.cricket_api_tools import (
    get_player_stats,
    get_team_squad,
    get_matchup_data,
    get_venue_stats
)
from tools.tactical_tools import (
    analyze_weaknesses,
    find_best_matchup,
    generate_bowling_plan,
    generate_fielding_plan
)

class TestCricketApiTools(unittest.TestCase):
    """Test cases for cricket API tools"""
    
    def test_get_player_stats_structure(self):
        """Test that get_player_stats returns properly structured data"""
        result = get_player_stats("Virat Kohli")
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("player_name", data)
        self.assertIn("recent_form", data)
        self.assertIn("weaknesses", data)
        self.assertIn("strengths", data)
        
        # Check data types
        self.assertIsInstance(data["recent_form"], dict)
        self.assertIsInstance(data["weaknesses"], dict)
        self.assertIsInstance(data["strengths"], dict)
    
    def test_get_team_squad_structure(self):
        """Test that get_team_squad returns properly structured data"""
        result = get_team_squad("India")
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("team_name", data)
        self.assertIn("squad", data)
        self.assertIn("recent_performance", data)
        self.assertIn("strengths", data)
        self.assertIn("weaknesses", data)
        
        # Check data types
        self.assertIsInstance(data["squad"], dict)
        self.assertIsInstance(data["recent_performance"], dict)
        self.assertIsInstance(data["strengths"], list)
        self.assertIsInstance(data["weaknesses"], list)
    
    def test_get_matchup_data_structure(self):
        """Test that get_matchup_data returns properly structured data"""
        result = get_matchup_data("India", "Australia")
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("head_to_head", data)
        self.assertIn("recent_encounters", data)
        self.assertIn("venue_analysis", data)
        self.assertIn("key_trends", data)
        
        # Check data types
        self.assertIsInstance(data["head_to_head"], dict)
        self.assertIsInstance(data["recent_encounters"], list)
        self.assertIsInstance(data["venue_analysis"], dict)
        self.assertIsInstance(data["key_trends"], list)
    
    def test_get_venue_stats_structure(self):
        """Test that get_venue_stats returns properly structured data"""
        result = get_venue_stats("Narendra Modi Stadium")
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("venue_name", data)
        self.assertIn("pitch_conditions", data)
        self.assertIn("average_scores", data)
        self.assertIn("weather_impact", data)
        
        # Check data types
        self.assertIsInstance(data["pitch_conditions"], dict)
        self.assertIsInstance(data["average_scores"], dict)
        self.assertIsInstance(data["weather_impact"], dict)

class TestTacticalTools(unittest.TestCase):
    """Test cases for tactical analysis tools"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_player_data = {
            "player_name": "Test Player",
            "recent_form": {
                "batting_average": 45.0,
                "strike_rate": 120.0
            },
            "weaknesses": {
                "against_spin": {
                    "average": 25.0,
                    "strike_rate": 85.0
                },
                "early_innings": {
                    "first_10_balls": {
                        "average": 15.0,
                        "strike_rate": 70.0
                    }
                }
            },
            "strengths": {
                "death_overs": {
                    "overs_16_20": {
                        "average": 40.0,
                        "strike_rate": 150.0
                    }
                }
            }
        }
    
    def test_analyze_weaknesses_structure(self):
        """Test that analyze_weaknesses returns properly structured data"""
        result = analyze_weaknesses(json.dumps(self.sample_player_data))
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("player_name", data)
        self.assertIn("overall_assessment", data)
        self.assertIn("key_weaknesses", data)
        self.assertIn("vulnerable_phases", data)
        self.assertIn("tactical_opportunities", data)
        self.assertIn("recommendations", data)
        
        # Check data types
        self.assertIsInstance(data["key_weaknesses"], list)
        self.assertIsInstance(data["vulnerable_phases"], list)
        self.assertIsInstance(data["tactical_opportunities"], list)
        self.assertIsInstance(data["recommendations"], list)
    
    def test_find_best_matchup_structure(self):
        """Test that find_best_matchup returns properly structured data"""
        player1_data = self.sample_player_data.copy()
        player2_data = self.sample_player_data.copy()
        player2_data["player_name"] = "Player 2"
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("player1", data)
        self.assertIn("player2", data)
        self.assertIn("matchup_assessment", data)
        self.assertIn("key_factors", data)
        self.assertIn("tactical_considerations", data)
        self.assertIn("recommendations", data)
        
        # Check data types
        self.assertIsInstance(data["key_factors"], list)
        self.assertIsInstance(data["tactical_considerations"], list)
        self.assertIsInstance(data["recommendations"], list)
    
    def test_generate_bowling_plan_structure(self):
        """Test that generate_bowling_plan returns properly structured data"""
        result = generate_bowling_plan(
            json.dumps(self.sample_player_data),
            "Test context"
        )
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("player_name", data)
        self.assertIn("context", data)
        self.assertIn("overall_strategy", data)
        self.assertIn("phase_plans", data)
        self.assertIn("field_placements", data)
        self.assertIn("bowler_assignments", data)
        self.assertIn("tactical_variations", data)
        
        # Check data types
        self.assertIsInstance(data["phase_plans"], dict)
        self.assertIsInstance(data["field_placements"], dict)
        self.assertIsInstance(data["bowler_assignments"], dict)
        self.assertIsInstance(data["tactical_variations"], list)
    
    def test_generate_fielding_plan_structure(self):
        """Test that generate_fielding_plan returns properly structured data"""
        bowling_plan = {
            "player_name": "Test Player",
            "overall_strategy": "Test strategy"
        }
        
        result = generate_fielding_plan(
            json.dumps(self.sample_player_data),
            json.dumps(bowling_plan)
        )
        data = json.loads(result)
        
        # Check required fields
        self.assertIn("player_name", data)
        self.assertIn("overall_approach", data)
        self.assertIn("phase_fielding", data)
        self.assertIn("key_positions", data)
        self.assertIn("tactical_adjustments", data)
        self.assertIn("communication_points", data)
        
        # Check data types
        self.assertIsInstance(data["phase_fielding"], dict)
        self.assertIsInstance(data["key_positions"], list)
        self.assertIsInstance(data["tactical_adjustments"], list)
        self.assertIsInstance(data["communication_points"], list)
    
    def test_error_handling(self):
        """Test error handling in tactical tools"""
        # Test with invalid JSON
        result = analyze_weaknesses("invalid json")
        data = json.loads(result)
        self.assertIn("error", data)
        
        # Test with empty data
        result = analyze_weaknesses("{}")
        data = json.loads(result)
        self.assertIn("player_name", data)
    
    def test_weakness_analysis_logic(self):
        """Test the logic of weakness analysis"""
        result = analyze_weaknesses(json.dumps(self.sample_player_data))
        data = json.loads(result)
        
        # Should identify weaknesses
        self.assertGreater(len(data["key_weaknesses"]), 0)
        
        # Should provide recommendations
        self.assertGreater(len(data["recommendations"]), 0)
    
    def test_matchup_analysis_logic(self):
        """Test the logic of matchup analysis"""
        player1_data = self.sample_player_data.copy()
        player2_data = self.sample_player_data.copy()
        player2_data["player_name"] = "Player 2"
        player2_data["recent_form"]["batting_average"] = 30.0
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        data = json.loads(result)
        
        # Should provide assessment
        self.assertIsNotNone(data["matchup_assessment"])
        
        # Should identify key factors
        self.assertIsInstance(data["key_factors"], list)

if __name__ == '__main__':
    unittest.main()
