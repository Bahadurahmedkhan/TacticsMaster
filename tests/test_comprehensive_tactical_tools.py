"""
Comprehensive Unit Tests for Tactical Analysis Tools

This module contains comprehensive unit tests for all tactical analysis tools including
analyze_weaknesses, find_best_matchup, generate_bowling_plan, and generate_fielding_plan
with various data scenarios and edge cases.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from typing import Dict, Any, List

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.tactical_tools import (
    analyze_weaknesses,
    find_best_matchup,
    generate_bowling_plan,
    generate_fielding_plan,
    _assess_player_overall,
    _identify_weaknesses,
    _identify_vulnerable_phases,
    _identify_tactical_opportunities,
    _generate_weakness_recommendations,
    _assess_matchup,
    _identify_key_factors,
    _generate_tactical_considerations,
    _generate_matchup_recommendations,
    _generate_overall_strategy,
    _generate_phase_plans,
    _generate_field_placements,
    _generate_bowler_assignments,
    _generate_tactical_variations,
    _generate_fielding_approach,
    _generate_phase_fielding,
    _identify_key_positions,
    _generate_fielding_adjustments,
    _generate_communication_points
)

class TestTacticalToolsComprehensive(unittest.TestCase):
    """Comprehensive test cases for tactical analysis tools"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_player_data = {
            "player_name": "Test Player",
            "recent_form": {
                "batting_average": 45.0,
                "strike_rate": 120.0,
                "bowling_average": 28.4,
                "economy_rate": 5.2
            },
            "weaknesses": {
                "against_spin": {
                    "average": 25.0,
                    "strike_rate": 85.0,
                    "dismissal_rate": 0.15
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
                }
            ]
        }
        
        self.sample_bowling_plan = {
            "player_name": "Test Player",
            "overall_strategy": "Attack early with pace bowling",
            "phase_plans": {
                "powerplay": {
                    "strategy": "Attack with pace bowling",
                    "field_setting": "Attacking field"
                }
            }
        }
    
    def test_analyze_weaknesses_success(self):
        """Test successful weakness analysis"""
        result = analyze_weaknesses(json.dumps(self.sample_player_data))
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Test Player")
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
    
    def test_analyze_weaknesses_empty_data(self):
        """Test weakness analysis with empty data"""
        result = analyze_weaknesses("")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_none_data(self):
        """Test weakness analysis with None data"""
        result = analyze_weaknesses(None)
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_invalid_json(self):
        """Test weakness analysis with invalid JSON"""
        result = analyze_weaknesses("invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_malformed_data(self):
        """Test weakness analysis with malformed data"""
        malformed_data = {"player_name": "Test", "invalid_field": "value"}
        result = analyze_weaknesses(json.dumps(malformed_data))
        
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Test")
    
    def test_analyze_weaknesses_minimal_data(self):
        """Test weakness analysis with minimal data"""
        minimal_data = {"player_name": "Test Player"}
        result = analyze_weaknesses(json.dumps(minimal_data))
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Test Player")
        self.assertIn("overall_assessment", data)
        self.assertIn("key_weaknesses", data)
    
    def test_find_best_matchup_success(self):
        """Test successful matchup analysis"""
        player1_data = self.sample_player_data.copy()
        player2_data = self.sample_player_data.copy()
        player2_data["player_name"] = "Player 2"
        player2_data["recent_form"]["batting_average"] = 30.0
        
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
        self.assertIn("matchup_assessment", data)
        self.assertIn("key_factors", data)
        self.assertIn("tactical_considerations", data)
        self.assertIn("recommendations", data)
        
        # Check data types
        self.assertIsInstance(data["key_factors"], list)
        self.assertIsInstance(data["tactical_considerations"], list)
        self.assertIsInstance(data["recommendations"], list)
    
    def test_find_best_matchup_invalid_data(self):
        """Test matchup analysis with invalid data"""
        result = find_best_matchup("invalid json", "invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_find_best_matchup_empty_data(self):
        """Test matchup analysis with empty data"""
        result = find_best_matchup("", "")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_find_best_matchup_same_players(self):
        """Test matchup analysis with same players"""
        result = find_best_matchup(
            json.dumps(self.sample_player_data),
            json.dumps(self.sample_player_data)
        )
        
        data = json.loads(result)
        self.assertIn("player1", data)
        self.assertIn("player2", data)
        self.assertIn("matchup_assessment", data)
    
    def test_generate_bowling_plan_success(self):
        """Test successful bowling plan generation"""
        result = generate_bowling_plan(
            json.dumps(self.sample_player_data),
            "Test context"
        )
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Test Player")
        self.assertIn("context", data)
        self.assertEqual(data["context"], "Test context")
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
    
    def test_generate_bowling_plan_invalid_data(self):
        """Test bowling plan generation with invalid data"""
        result = generate_bowling_plan("invalid json", "Test context")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_bowling_plan_empty_context(self):
        """Test bowling plan generation with empty context"""
        result = generate_bowling_plan(
            json.dumps(self.sample_player_data),
            ""
        )
        
        data = json.loads(result)
        self.assertEqual(data["context"], "")
        self.assertIn("overall_strategy", data)
    
    def test_generate_bowling_plan_none_context(self):
        """Test bowling plan generation with None context"""
        result = generate_bowling_plan(
            json.dumps(self.sample_player_data),
            None
        )
        
        data = json.loads(result)
        self.assertIsNone(data["context"])
        self.assertIn("overall_strategy", data)
    
    def test_generate_fielding_plan_success(self):
        """Test successful fielding plan generation"""
        result = generate_fielding_plan(
            json.dumps(self.sample_player_data),
            json.dumps(self.sample_bowling_plan)
        )
        
        # Should return JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertEqual(data["player_name"], "Test Player")
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
    
    def test_generate_fielding_plan_invalid_data(self):
        """Test fielding plan generation with invalid data"""
        result = generate_fielding_plan("invalid json", "invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_fielding_plan_empty_bowling_plan(self):
        """Test fielding plan generation with empty bowling plan"""
        result = generate_fielding_plan(
            json.dumps(self.sample_player_data),
            ""
        )
        
        data = json.loads(result)
        self.assertIn("error", data)

class TestTacticalToolsHelperFunctions(unittest.TestCase):
    """Test helper functions for tactical analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_data = {
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
    
    def test_assess_player_overall_excellent_form(self):
        """Test player assessment with excellent form"""
        data = {
            "recent_form": {
                "batting_average": 55.0,
                "strike_rate": 125.0
            }
        }
        
        result = _assess_player_overall(data)
        self.assertIn("Excellent form", result)
    
    def test_assess_player_overall_good_form(self):
        """Test player assessment with good form"""
        data = {
            "recent_form": {
                "batting_average": 45.0,
                "strike_rate": 115.0
            }
        }
        
        result = _assess_player_overall(data)
        self.assertIn("Good form", result)
    
    def test_assess_player_overall_moderate_form(self):
        """Test player assessment with moderate form"""
        data = {
            "recent_form": {
                "batting_average": 35.0,
                "strike_rate": 105.0
            }
        }
        
        result = _assess_player_overall(data)
        self.assertIn("Moderate form", result)
    
    def test_assess_player_overall_poor_form(self):
        """Test player assessment with poor form"""
        data = {
            "recent_form": {
                "batting_average": 25.0,
                "strike_rate": 95.0
            }
        }
        
        result = _assess_player_overall(data)
        self.assertIn("Poor form", result)
    
    def test_assess_player_overall_missing_data(self):
        """Test player assessment with missing data"""
        data = {}
        
        result = _assess_player_overall(data)
        self.assertIn("Poor form", result)
    
    def test_identify_weaknesses(self):
        """Test weakness identification"""
        result = _identify_weaknesses(self.sample_data)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Should identify spin weakness
        spin_weakness_found = any("spin" in weakness.lower() for weakness in result)
        self.assertTrue(spin_weakness_found)
    
    def test_identify_weaknesses_no_weaknesses(self):
        """Test weakness identification with no weaknesses"""
        data = {"weaknesses": {}}
        
        result = _identify_weaknesses(data)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_identify_vulnerable_phases(self):
        """Test vulnerable phase identification"""
        result = _identify_vulnerable_phases(self.sample_data)
        
        self.assertIsInstance(result, list)
        # Should identify early innings weakness
        early_weakness_found = any("early" in phase.lower() or "first" in phase.lower() for phase in result)
        self.assertTrue(early_weakness_found)
    
    def test_identify_vulnerable_phases_no_weaknesses(self):
        """Test vulnerable phase identification with no weaknesses"""
        data = {"recent_form": {"strike_rate": 120.0}}
        
        result = _identify_vulnerable_phases(data)
        
        self.assertIsInstance(result, list)
    
    def test_identify_tactical_opportunities(self):
        """Test tactical opportunity identification"""
        result = _identify_tactical_opportunities(self.sample_data)
        
        self.assertIsInstance(result, list)
        # Should identify death overs opportunity
        death_opportunity_found = any("death" in opportunity.lower() for opportunity in result)
        self.assertTrue(death_opportunity_found)
    
    def test_identify_tactical_opportunities_no_strengths(self):
        """Test tactical opportunity identification with no strengths"""
        data = {"strengths": {}}
        
        result = _identify_tactical_opportunities(data)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_generate_weakness_recommendations(self):
        """Test weakness recommendation generation"""
        result = _generate_weakness_recommendations(self.sample_data)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Should recommend spin bowling
        spin_recommendation_found = any("spin" in rec.lower() for rec in result)
        self.assertTrue(spin_recommendation_found)
    
    def test_generate_weakness_recommendations_no_weaknesses(self):
        """Test weakness recommendation generation with no weaknesses"""
        data = {"weaknesses": {}}
        
        result = _generate_weakness_recommendations(data)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_assess_matchup(self):
        """Test matchup assessment"""
        data1 = {"player_name": "Player 1", "recent_form": {"batting_average": 50.0}}
        data2 = {"player_name": "Player 2", "recent_form": {"batting_average": 30.0}}
        
        result = _assess_matchup(data1, data2)
        
        self.assertIsInstance(result, str)
        self.assertIn("Player 1", result)
        self.assertIn("advantage", result)
    
    def test_assess_matchup_even_match(self):
        """Test matchup assessment with even match"""
        data1 = {"player_name": "Player 1", "recent_form": {"batting_average": 40.0}}
        data2 = {"player_name": "Player 2", "recent_form": {"batting_average": 42.0}}
        
        result = _assess_matchup(data1, data2)
        
        self.assertIsInstance(result, str)
        self.assertIn("Evenly matched", result)
    
    def test_identify_key_factors(self):
        """Test key factor identification"""
        data1 = {
            "strengths": {"against_pace": {"average": 50.0}},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        data2 = {
            "strengths": {"against_spin": {"average": 45.0}},
            "weaknesses": {"against_pace": {"average": 20.0}}
        }
        
        result = _identify_key_factors(data1, data2)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_tactical_considerations(self):
        """Test tactical consideration generation"""
        data1 = {"player_name": "Player 1"}
        data2 = {"player_name": "Player 2"}
        
        result = _generate_tactical_considerations(data1, data2)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_matchup_recommendations(self):
        """Test matchup recommendation generation"""
        data1 = {"player_name": "Player 1"}
        data2 = {"player_name": "Player 2"}
        
        result = _generate_matchup_recommendations(data1, data2)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_overall_strategy(self):
        """Test overall strategy generation"""
        result = _generate_overall_strategy(self.sample_data, "Test context")
        
        self.assertIsInstance(result, str)
        self.assertIn("Attack", result)
        self.assertIn("pace", result)
    
    def test_generate_phase_plans(self):
        """Test phase plan generation"""
        result = _generate_phase_plans(self.sample_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn("powerplay", result)
        self.assertIn("middle_overs", result)
        self.assertIn("death_overs", result)
        
        # Check each phase has required fields
        for phase in result.values():
            self.assertIn("strategy", phase)
            self.assertIn("field_setting", phase)
            self.assertIn("key_bowlers", phase)
    
    def test_generate_field_placements(self):
        """Test field placement generation"""
        result = _generate_field_placements(self.sample_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn("powerplay", result)
        self.assertIn("middle_overs", result)
        self.assertIn("death_overs", result)
        
        # Check each phase has list of positions
        for positions in result.values():
            self.assertIsInstance(positions, list)
    
    def test_generate_bowler_assignments(self):
        """Test bowler assignment generation"""
        result = _generate_bowler_assignments(self.sample_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn("powerplay", result)
        self.assertIn("middle_overs", result)
        self.assertIn("death_overs", result)
        
        # Check each phase has list of bowlers
        for bowlers in result.values():
            self.assertIsInstance(bowlers, list)
    
    def test_generate_tactical_variations(self):
        """Test tactical variation generation"""
        result = _generate_tactical_variations(self.sample_data)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_fielding_approach(self):
        """Test fielding approach generation"""
        result = _generate_fielding_approach(self.sample_data, {})
        
        self.assertIsInstance(result, str)
        self.assertIn("fielding", result)
    
    def test_generate_phase_fielding(self):
        """Test phase fielding generation"""
        result = _generate_phase_fielding(self.sample_data, {})
        
        self.assertIsInstance(result, dict)
        self.assertIn("powerplay", result)
        self.assertIn("middle_overs", result)
        self.assertIn("death_overs", result)
        
        # Check each phase has required fields
        for phase in result.values():
            self.assertIn("field_setting", phase)
            self.assertIn("key_positions", phase)
    
    def test_identify_key_positions(self):
        """Test key position identification"""
        result = _identify_key_positions(self.sample_data, {})
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_fielding_adjustments(self):
        """Test fielding adjustment generation"""
        result = _generate_fielding_adjustments(self.sample_data, {})
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_generate_communication_points(self):
        """Test communication point generation"""
        result = _generate_communication_points(self.sample_data, {})
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

class TestTacticalToolsEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios for tactical tools"""
    
    def test_analyze_weaknesses_very_large_data(self):
        """Test weakness analysis with very large data"""
        large_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {f"weakness_{i}": {"average": i} for i in range(1000)},
            "strengths": {f"strength_{i}": {"average": i} for i in range(1000)}
        }
        
        result = analyze_weaknesses(json.dumps(large_data))
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Test Player")
        self.assertIn("overall_assessment", data)
    
    def test_analyze_weaknesses_deeply_nested_data(self):
        """Test weakness analysis with deeply nested data"""
        nested_data = {
            "player_name": "Test Player",
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "value": "deep"
                            }
                        }
                    }
                }
            }
        }
        
        result = analyze_weaknesses(json.dumps(nested_data))
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Test Player")
        self.assertIn("overall_assessment", data)
    
    def test_analyze_weaknesses_unicode_data(self):
        """Test weakness analysis with unicode data"""
        unicode_data = {
            "player_name": "Test Player 测试",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_spin": {"average": 25.0}},
            "strengths": {"against_pace": {"average": 50.0}}
        }
        
        result = analyze_weaknesses(json.dumps(unicode_data))
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Test Player 测试")
        self.assertIn("overall_assessment", data)
    
    def test_analyze_weaknesses_special_characters(self):
        """Test weakness analysis with special characters"""
        special_data = {
            "player_name": "Test Player!@#$%^&*()",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_spin": {"average": 25.0}},
            "strengths": {"against_pace": {"average": 50.0}}
        }
        
        result = analyze_weaknesses(json.dumps(special_data))
        
        data = json.loads(result)
        self.assertEqual(data["player_name"], "Test Player!@#$%^&*()")
        self.assertIn("overall_assessment", data)
    
    def test_find_best_matchup_very_different_players(self):
        """Test matchup analysis with very different players"""
        player1_data = {
            "player_name": "Player 1",
            "recent_form": {"batting_average": 60.0, "strike_rate": 140.0}
        }
        player2_data = {
            "player_name": "Player 2",
            "recent_form": {"batting_average": 20.0, "strike_rate": 80.0}
        }
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        
        data = json.loads(result)
        self.assertIn("player1", data)
        self.assertIn("player2", data)
        self.assertIn("matchup_assessment", data)
    
    def test_generate_bowling_plan_complex_context(self):
        """Test bowling plan generation with complex context"""
        complex_context = "Test context with special characters: !@#$%^&*() and unicode: 你好世界"
        
        result = generate_bowling_plan(
            json.dumps(self.sample_player_data),
            complex_context
        )
        
        data = json.loads(result)
        self.assertEqual(data["context"], complex_context)
        self.assertIn("overall_strategy", data)
    
    def test_generate_fielding_plan_mismatched_data(self):
        """Test fielding plan generation with mismatched data"""
        different_bowling_plan = {
            "player_name": "Different Player",
            "overall_strategy": "Different strategy"
        }
        
        result = generate_fielding_plan(
            json.dumps(self.sample_player_data),
            json.dumps(different_bowling_plan)
        )
        
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertIn("overall_approach", data)

if __name__ == '__main__':
    unittest.main()
