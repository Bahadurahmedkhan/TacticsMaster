"""
Comprehensive Unit Tests for Tactical Analysis Tools

This module contains detailed unit tests for all tactical analysis tools,
covering functionality, error handling, and edge cases.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from app.tools.tactical_tools import (
    analyze_weaknesses,
    find_best_matchup,
    generate_bowling_plan,
    generate_fielding_plan
)


class TestAnalyzeWeaknesses:
    """Test analyze_weaknesses tool functionality"""
    
    def test_analyze_weaknesses_success(self, sample_player_data):
        """Test successful weakness analysis"""
        player_json = json.dumps(sample_player_data)
        result = analyze_weaknesses(player_json)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli"
        assert "key_weaknesses" in data
        assert "recommendations" in data
        assert "analysis_summary" in data
    
    def test_analyze_weaknesses_with_invalid_json(self):
        """Test weakness analysis with invalid JSON"""
        result = analyze_weaknesses("invalid json")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid JSON" in data["error"]
    
    def test_analyze_weaknesses_with_empty_string(self):
        """Test weakness analysis with empty string"""
        result = analyze_weaknesses("")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Empty input" in data["error"]
    
    def test_analyze_weaknesses_with_none_input(self):
        """Test weakness analysis with None input"""
        result = analyze_weaknesses(None)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid input" in data["error"]
    
    def test_analyze_weaknesses_with_missing_fields(self):
        """Test weakness analysis with missing required fields"""
        incomplete_data = {"player_name": "Test Player"}
        result = analyze_weaknesses(json.dumps(incomplete_data))
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Missing required fields" in data["error"]
    
    def test_analyze_weaknesses_with_special_characters(self):
        """Test weakness analysis with special characters in player name"""
        player_data = {
            "player_name": "Virat Kohli!@#$%^&*()",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        result = analyze_weaknesses(json.dumps(player_data))
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli!@#$%^&*()"
    
    def test_analyze_weaknesses_with_unicode_characters(self):
        """Test weakness analysis with unicode characters in player name"""
        player_data = {
            "player_name": "Virat Kohli 维拉特·科利",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        result = analyze_weaknesses(json.dumps(player_data))
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli 维拉特·科利"
    
    def test_analyze_weaknesses_with_complex_weaknesses(self):
        """Test weakness analysis with complex weakness data"""
        complex_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {
                "against_spin": {"average": 25.0, "strike_rate": 80.0},
                "early_innings": {"first_10_balls": {"average": 15.0}},
                "against_bounce": {"average": 20.0}
            }
        }
        result = analyze_weaknesses(json.dumps(complex_data))
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert len(data["key_weaknesses"]) > 0
        assert len(data["recommendations"]) > 0
    
    def test_analyze_weaknesses_with_no_weaknesses(self):
        """Test weakness analysis with no weaknesses data"""
        no_weaknesses_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {}
        }
        result = analyze_weaknesses(json.dumps(no_weaknesses_data))
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Test Player"
        assert "No significant weaknesses identified" in data["analysis_summary"]


class TestFindBestMatchup:
    """Test find_best_matchup tool functionality"""
    
    def test_find_best_matchup_success(self, sample_player_data):
        """Test successful matchup analysis"""
        player1_json = json.dumps(sample_player_data)
        player2_data = {
            "player_name": "Rohit Sharma",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        player2_json = json.dumps(player2_data)
        
        result = find_best_matchup(player1_json, player2_json)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "player1" in data
        assert "player2" in data
        assert "matchup_assessment" in data
        assert "recommendations" in data
    
    def test_find_best_matchup_with_invalid_json(self):
        """Test matchup analysis with invalid JSON"""
        result = find_best_matchup("invalid json", "invalid json")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid JSON" in data["error"]
    
    def test_find_best_matchup_with_empty_strings(self):
        """Test matchup analysis with empty strings"""
        result = find_best_matchup("", "")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Empty input" in data["error"]
    
    def test_find_best_matchup_with_none_inputs(self):
        """Test matchup analysis with None inputs"""
        result = find_best_matchup(None, None)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid input" in data["error"]
    
    def test_find_best_matchup_with_missing_fields(self):
        """Test matchup analysis with missing required fields"""
        incomplete_data1 = {"player_name": "Player 1"}
        incomplete_data2 = {"player_name": "Player 2"}
        
        result = find_best_matchup(
            json.dumps(incomplete_data1),
            json.dumps(incomplete_data2)
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Missing required fields" in data["error"]
    
    def test_find_best_matchup_with_special_characters(self):
        """Test matchup analysis with special characters in player names"""
        player1_data = {
            "player_name": "Virat Kohli!@#$%^&*()",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        player2_data = {
            "player_name": "Rohit Sharma!@#$%^&*()",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "Virat Kohli!@#$%^&*()" in data["player1"]
        assert "Rohit Sharma!@#$%^&*()" in data["player2"]
    
    def test_find_best_matchup_with_unicode_characters(self):
        """Test matchup analysis with unicode characters in player names"""
        player1_data = {
            "player_name": "Virat Kohli 维拉特·科利",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        player2_data = {
            "player_name": "Rohit Sharma 罗希特·夏尔马",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        
        result = find_best_matchup(
            json.dumps(player1_data),
            json.dumps(player2_data)
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "Virat Kohli 维拉特·科利" in data["player1"]
        assert "Rohit Sharma 罗希特·夏尔马" in data["player2"]
    
    def test_find_best_matchup_with_complex_data(self):
        """Test matchup analysis with complex player data"""
        complex_data1 = {
            "player_name": "Player 1",
            "recent_form": {"batting_average": 50.0, "strike_rate": 120.0},
            "weaknesses": {
                "against_spin": {"average": 25.0, "strike_rate": 80.0},
                "early_innings": {"first_10_balls": {"average": 15.0}}
            },
            "strengths": {"death_overs": {"average": 45.0}}
        }
        complex_data2 = {
            "player_name": "Player 2",
            "recent_form": {"batting_average": 45.0, "strike_rate": 110.0},
            "weaknesses": {
                "against_pace": {"average": 30.0, "strike_rate": 85.0},
                "against_bounce": {"average": 20.0}
            },
            "strengths": {"powerplay": {"average": 55.0}}
        }
        
        result = find_best_matchup(
            json.dumps(complex_data1),
            json.dumps(complex_data2)
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert len(data["matchup_assessment"]) > 0
        assert len(data["recommendations"]) > 0


class TestGenerateBowlingPlan:
    """Test generate_bowling_plan tool functionality"""
    
    def test_generate_bowling_plan_success(self, sample_player_data):
        """Test successful bowling plan generation"""
        player_json = json.dumps(sample_player_data)
        context = "Test bowling context"
        
        result = generate_bowling_plan(player_json, context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli"
        assert "overall_strategy" in data
        assert "phase_plans" in data
        assert "key_tactics" in data
    
    def test_generate_bowling_plan_with_invalid_json(self):
        """Test bowling plan generation with invalid JSON"""
        result = generate_bowling_plan("invalid json", "context")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid JSON" in data["error"]
    
    def test_generate_bowling_plan_with_empty_strings(self):
        """Test bowling plan generation with empty strings"""
        result = generate_bowling_plan("", "")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Empty input" in data["error"]
    
    def test_generate_bowling_plan_with_none_inputs(self):
        """Test bowling plan generation with None inputs"""
        result = generate_bowling_plan(None, None)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid input" in data["error"]
    
    def test_generate_bowling_plan_with_missing_fields(self):
        """Test bowling plan generation with missing required fields"""
        incomplete_data = {"player_name": "Test Player"}
        result = generate_bowling_plan(json.dumps(incomplete_data), "context")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Missing required fields" in data["error"]
    
    def test_generate_bowling_plan_with_special_characters(self):
        """Test bowling plan generation with special characters"""
        player_data = {
            "player_name": "Virat Kohli!@#$%^&*()",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        context = "Test context!@#$%^&*()"
        
        result = generate_bowling_plan(json.dumps(player_data), context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli!@#$%^&*()"
    
    def test_generate_bowling_plan_with_unicode_characters(self):
        """Test bowling plan generation with unicode characters"""
        player_data = {
            "player_name": "Virat Kohli 维拉特·科利",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        context = "Test context 测试上下文"
        
        result = generate_bowling_plan(json.dumps(player_data), context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli 维拉特·科利"
    
    def test_generate_bowling_plan_with_complex_data(self):
        """Test bowling plan generation with complex player data"""
        complex_data = {
            "player_name": "Test Player",
            "recent_form": {
                "batting_average": 50.0,
                "strike_rate": 120.0,
                "bowling_average": 25.0
            },
            "weaknesses": {
                "against_spin": {"average": 25.0, "strike_rate": 80.0},
                "early_innings": {"first_10_balls": {"average": 15.0}},
                "against_bounce": {"average": 20.0}
            },
            "strengths": {
                "death_overs": {"average": 45.0, "strike_rate": 140.0},
                "against_pace": {"average": 55.0, "strike_rate": 130.0}
            }
        }
        context = "Complex bowling context with multiple factors"
        
        result = generate_bowling_plan(json.dumps(complex_data), context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert len(data["phase_plans"]) > 0
        assert len(data["key_tactics"]) > 0
    
    def test_generate_bowling_plan_with_long_context(self):
        """Test bowling plan generation with long context"""
        player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        long_context = "Test context " * 1000  # Very long context
        
        result = generate_bowling_plan(json.dumps(player_data), long_context)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Test Player"


class TestGenerateFieldingPlan:
    """Test generate_fielding_plan tool functionality"""
    
    def test_generate_fielding_plan_success(self, sample_player_data):
        """Test successful fielding plan generation"""
        player_json = json.dumps(sample_player_data)
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy",
            "phase_plans": {"powerplay": "Test plan"}
        })
        
        result = generate_fielding_plan(player_json, bowling_plan)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli"
        assert "overall_approach" in data
        assert "phase_fielding" in data
        assert "key_positions" in data
    
    def test_generate_fielding_plan_with_invalid_json(self):
        """Test fielding plan generation with invalid JSON"""
        result = generate_fielding_plan("invalid json", "invalid json")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid JSON" in data["error"]
    
    def test_generate_fielding_plan_with_empty_strings(self):
        """Test fielding plan generation with empty strings"""
        result = generate_fielding_plan("", "")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Empty input" in data["error"]
    
    def test_generate_fielding_plan_with_none_inputs(self):
        """Test fielding plan generation with None inputs"""
        result = generate_fielding_plan(None, None)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid input" in data["error"]
    
    def test_generate_fielding_plan_with_missing_fields(self):
        """Test fielding plan generation with missing required fields"""
        incomplete_data = {"player_name": "Test Player"}
        result = generate_fielding_plan(json.dumps(incomplete_data), "{}")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Missing required fields" in data["error"]
    
    def test_generate_fielding_plan_with_special_characters(self):
        """Test fielding plan generation with special characters"""
        player_data = {
            "player_name": "Virat Kohli!@#$%^&*()",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy!@#$%^&*()",
            "phase_plans": {"powerplay": "Test plan!@#$%^&*()"}
        })
        
        result = generate_fielding_plan(json.dumps(player_data), bowling_plan)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli!@#$%^&*()"
    
    def test_generate_fielding_plan_with_unicode_characters(self):
        """Test fielding plan generation with unicode characters"""
        player_data = {
            "player_name": "Virat Kohli 维拉特·科利",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy 测试策略",
            "phase_plans": {"powerplay": "Test plan 测试计划"}
        })
        
        result = generate_fielding_plan(json.dumps(player_data), bowling_plan)
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert data["player_name"] == "Virat Kohli 维拉特·科利"
    
    def test_generate_fielding_plan_with_complex_data(self):
        """Test fielding plan generation with complex data"""
        complex_player_data = {
            "player_name": "Test Player",
            "recent_form": {
                "batting_average": 50.0,
                "strike_rate": 120.0
            },
            "weaknesses": {
                "against_spin": {"average": 25.0, "strike_rate": 80.0},
                "early_innings": {"first_10_balls": {"average": 15.0}}
            },
            "strengths": {
                "death_overs": {"average": 45.0, "strike_rate": 140.0}
            }
        }
        complex_bowling_plan = {
            "overall_strategy": "Complex bowling strategy",
            "phase_plans": {
                "powerplay": "Aggressive bowling",
                "middle_overs": "Controlled bowling",
                "death_overs": "Defensive bowling"
            },
            "key_tactics": ["Use variations", "Maintain pressure"]
        }
        
        result = generate_fielding_plan(
            json.dumps(complex_player_data),
            json.dumps(complex_bowling_plan)
        )
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert len(data["phase_fielding"]) > 0
        assert len(data["key_positions"]) > 0
    
    def test_generate_fielding_plan_with_invalid_bowling_plan(self):
        """Test fielding plan generation with invalid bowling plan"""
        player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 50.0},
            "weaknesses": {"against_spin": {"average": 25.0}}
        }
        
        result = generate_fielding_plan(json.dumps(player_data), "invalid json")
        
        assert isinstance(result, str)
        data = json.loads(result)
        assert "error" in data
        assert "Invalid bowling plan JSON" in data["error"]


class TestTacticalToolsPerformance:
    """Test tactical tools performance"""
    
    def test_analyze_weaknesses_performance(self, sample_player_data):
        """Test analyze_weaknesses performance"""
        import time
        
        player_json = json.dumps(sample_player_data)
        
        start_time = time.time()
        
        for _ in range(10):
            result = analyze_weaknesses(player_json)
            assert isinstance(result, str)
        
        end_time = time.time()
        
        # Should complete 10 calls in less than 1 second
        assert (end_time - start_time) < 1.0
    
    def test_find_best_matchup_performance(self, sample_player_data):
        """Test find_best_matchup performance"""
        import time
        
        player1_json = json.dumps(sample_player_data)
        player2_data = {
            "player_name": "Rohit Sharma",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        player2_json = json.dumps(player2_data)
        
        start_time = time.time()
        
        for _ in range(10):
            result = find_best_matchup(player1_json, player2_json)
            assert isinstance(result, str)
        
        end_time = time.time()
        
        # Should complete 10 calls in less than 1 second
        assert (end_time - start_time) < 1.0
    
    def test_generate_bowling_plan_performance(self, sample_player_data):
        """Test generate_bowling_plan performance"""
        import time
        
        player_json = json.dumps(sample_player_data)
        context = "Test context"
        
        start_time = time.time()
        
        for _ in range(10):
            result = generate_bowling_plan(player_json, context)
            assert isinstance(result, str)
        
        end_time = time.time()
        
        # Should complete 10 calls in less than 1 second
        assert (end_time - start_time) < 1.0
    
    def test_generate_fielding_plan_performance(self, sample_player_data):
        """Test generate_fielding_plan performance"""
        import time
        
        player_json = json.dumps(sample_player_data)
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy",
            "phase_plans": {"powerplay": "Test plan"}
        })
        
        start_time = time.time()
        
        for _ in range(10):
            result = generate_fielding_plan(player_json, bowling_plan)
            assert isinstance(result, str)
        
        end_time = time.time()
        
        # Should complete 10 calls in less than 1 second
        assert (end_time - start_time) < 1.0


class TestTacticalToolsMemoryUsage:
    """Test tactical tools memory usage"""
    
    def test_analyze_weaknesses_memory_usage(self, sample_player_data):
        """Test analyze_weaknesses memory usage"""
        import sys
        
        player_json = json.dumps(sample_player_data)
        result = analyze_weaknesses(player_json)
        
        # Result should not be excessively large
        assert sys.getsizeof(result) < 10000  # Less than 10KB
    
    def test_find_best_matchup_memory_usage(self, sample_player_data):
        """Test find_best_matchup memory usage"""
        import sys
        
        player1_json = json.dumps(sample_player_data)
        player2_data = {
            "player_name": "Rohit Sharma",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        player2_json = json.dumps(player2_data)
        
        result = find_best_matchup(player1_json, player2_json)
        
        # Result should not be excessively large
        assert sys.getsizeof(result) < 10000  # Less than 10KB
    
    def test_generate_bowling_plan_memory_usage(self, sample_player_data):
        """Test generate_bowling_plan memory usage"""
        import sys
        
        player_json = json.dumps(sample_player_data)
        context = "Test context"
        
        result = generate_bowling_plan(player_json, context)
        
        # Result should not be excessively large
        assert sys.getsizeof(result) < 10000  # Less than 10KB
    
    def test_generate_fielding_plan_memory_usage(self, sample_player_data):
        """Test generate_fielding_plan memory usage"""
        import sys
        
        player_json = json.dumps(sample_player_data)
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy",
            "phase_plans": {"powerplay": "Test plan"}
        })
        
        result = generate_fielding_plan(player_json, bowling_plan)
        
        # Result should not be excessively large
        assert sys.getsizeof(result) < 10000  # Less than 10KB


class TestTacticalToolsDataValidation:
    """Test tactical tools data validation"""
    
    def test_analyze_weaknesses_data_structure(self, sample_player_data):
        """Test analyze_weaknesses data structure validation"""
        player_json = json.dumps(sample_player_data)
        result = analyze_weaknesses(player_json)
        data = json.loads(result)
        
        # Validate required fields
        assert "player_name" in data
        assert "key_weaknesses" in data
        assert "recommendations" in data
        assert "analysis_summary" in data
        
        # Validate data types
        assert isinstance(data["player_name"], str)
        assert isinstance(data["key_weaknesses"], list)
        assert isinstance(data["recommendations"], list)
        assert isinstance(data["analysis_summary"], str)
    
    def test_find_best_matchup_data_structure(self, sample_player_data):
        """Test find_best_matchup data structure validation"""
        player1_json = json.dumps(sample_player_data)
        player2_data = {
            "player_name": "Rohit Sharma",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {"against_pace": {"average": 30.0}}
        }
        player2_json = json.dumps(player2_data)
        
        result = find_best_matchup(player1_json, player2_json)
        data = json.loads(result)
        
        # Validate required fields
        assert "player1" in data
        assert "player2" in data
        assert "matchup_assessment" in data
        assert "recommendations" in data
        
        # Validate data types
        assert isinstance(data["player1"], str)
        assert isinstance(data["player2"], str)
        assert isinstance(data["matchup_assessment"], str)
        assert isinstance(data["recommendations"], list)
    
    def test_generate_bowling_plan_data_structure(self, sample_player_data):
        """Test generate_bowling_plan data structure validation"""
        player_json = json.dumps(sample_player_data)
        context = "Test context"
        
        result = generate_bowling_plan(player_json, context)
        data = json.loads(result)
        
        # Validate required fields
        assert "player_name" in data
        assert "overall_strategy" in data
        assert "phase_plans" in data
        assert "key_tactics" in data
        
        # Validate data types
        assert isinstance(data["player_name"], str)
        assert isinstance(data["overall_strategy"], str)
        assert isinstance(data["phase_plans"], dict)
        assert isinstance(data["key_tactics"], list)
    
    def test_generate_fielding_plan_data_structure(self, sample_player_data):
        """Test generate_fielding_plan data structure validation"""
        player_json = json.dumps(sample_player_data)
        bowling_plan = json.dumps({
            "overall_strategy": "Test strategy",
            "phase_plans": {"powerplay": "Test plan"}
        })
        
        result = generate_fielding_plan(player_json, bowling_plan)
        data = json.loads(result)
        
        # Validate required fields
        assert "player_name" in data
        assert "overall_approach" in data
        assert "phase_fielding" in data
        assert "key_positions" in data
        
        # Validate data types
        assert isinstance(data["player_name"], str)
        assert isinstance(data["overall_approach"], str)
        assert isinstance(data["phase_fielding"], dict)
        assert isinstance(data["key_positions"], list)
