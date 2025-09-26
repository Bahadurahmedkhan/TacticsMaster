"""
Comprehensive Integration Tests for Tactics Master System

This module contains detailed integration tests that test the complete workflow
from API calls to response generation, including end-to-end scenarios.
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, Any, List
from fastapi.testclient import TestClient

# Add the necessary paths
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Mock the hybrid_agent import before importing main
with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
    from backend.main import app

from app.agent import TacticsMasterAgent
from app.tools.cricket_api_tools import get_player_stats, get_team_squad, get_matchup_data, get_venue_stats
from app.tools.tactical_tools import analyze_weaknesses, find_best_matchup, generate_bowling_plan, generate_fielding_plan


class TestCompleteWorkflowIntegration:
    """Test complete workflow integration scenarios"""
    
    def test_complete_analysis_workflow(self, test_client, sample_analysis_response):
        """Test complete analysis workflow from API to response"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=sample_analysis_response)
            
            request_data = {
                "query": "Analyze Virat Kohli's batting weaknesses against Australia",
                "context": {
                    "team": "India",
                    "opponent": "Australia",
                    "venue": "Narendra Modi Stadium"
                }
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert data["response"] == "Comprehensive analysis of Virat Kohli's batting weaknesses"
            assert data["analysis"]["player_name"] == "Virat Kohli"
            assert data["sources"] == ["CricAPI", "Historical Data", "Tactical Analysis"]
            
            # Verify agent was called with correct parameters
            mock_agent.analyze.assert_called_once_with(
                "Analyze Virat Kohli's batting weaknesses against Australia",
                {
                    "team": "India",
                    "opponent": "Australia",
                    "venue": "Narendra Modi Stadium"
                }
            )
    
    def test_cricket_api_tools_integration(self):
        """Test integration between cricket API tools"""
        # Test player stats
        player_stats = get_player_stats("Virat Kohli")
        assert isinstance(player_stats, str)
        player_data = json.loads(player_stats)
        assert "player_name" in player_data
        assert "recent_form" in player_data
        assert player_data["player_name"] == "Virat Kohli"
        
        # Test team squad
        team_squad = get_team_squad("India")
        assert isinstance(team_squad, str)
        team_data = json.loads(team_squad)
        assert "team_name" in team_data
        assert "squad" in team_data
        assert team_data["team_name"] == "India"
        
        # Test matchup data
        matchup_data = get_matchup_data("India", "Australia")
        assert isinstance(matchup_data, str)
        matchup_result = json.loads(matchup_data)
        assert "head_to_head" in matchup_result
        assert "recent_encounters" in matchup_result
        
        # Test venue stats
        venue_stats = get_venue_stats("Narendra Modi Stadium")
        assert isinstance(venue_stats, str)
        venue_data = json.loads(venue_stats)
        assert "venue_name" in venue_data
        assert "pitch_conditions" in venue_data
        assert venue_data["venue_name"] == "Narendra Modi Stadium"
    
    def test_tactical_tools_integration(self):
        """Test integration between tactical analysis tools"""
        # Get player data
        player_stats = get_player_stats("Virat Kohli")
        player_data = json.loads(player_stats)
        
        # Test weakness analysis
        weakness_analysis = analyze_weaknesses(player_stats)
        assert isinstance(weakness_analysis, str)
        weakness_data = json.loads(weakness_analysis)
        assert "player_name" in weakness_data
        assert "key_weaknesses" in weakness_data
        assert "recommendations" in weakness_data
        assert weakness_data["player_name"] == "Virat Kohli"
        
        # Test matchup analysis
        player2_stats = get_player_stats("Rohit Sharma")
        matchup_analysis = find_best_matchup(player_stats, player2_stats)
        assert isinstance(matchup_analysis, str)
        matchup_data = json.loads(matchup_analysis)
        assert "player1" in matchup_data
        assert "player2" in matchup_data
        assert "matchup_assessment" in matchup_data
        
        # Test bowling plan generation
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        assert isinstance(bowling_plan, str)
        bowling_data = json.loads(bowling_plan)
        assert "player_name" in bowling_data
        assert "overall_strategy" in bowling_data
        assert "phase_plans" in bowling_data
        assert bowling_data["player_name"] == "Virat Kohli"
        
        # Test fielding plan generation
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        assert isinstance(fielding_plan, str)
        fielding_data = json.loads(fielding_plan)
        assert "player_name" in fielding_data
        assert "overall_approach" in fielding_data
        assert "phase_fielding" in fielding_data
        assert fielding_data["player_name"] == "Virat Kohli"
    
    def test_agent_tools_integration(self, mock_llm, mock_tools):
        """Test integration between agent and tools"""
        # Create agent
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Test agent initialization
        assert agent.llm == mock_llm
        assert agent.tools == mock_tools
        assert agent.verbose is True
        
        # Test agent info
        info = agent.get_agent_info()
        assert info["name"] == "Tactics Master"
        assert info["version"] == "1.0.0"
        assert "cricket" in info["description"].lower()
        assert len(info["available_tools"]) == len(mock_tools)
    
    def test_backend_health_integration(self, test_client):
        """Test backend health integration"""
        # Test health endpoint
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "agent_available" in data
        assert "timestamp" in data
    
    def test_backend_root_integration(self, test_client):
        """Test backend root endpoint integration"""
        # Test root endpoint
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["version"] == "1.0.0"
    
    def test_data_flow_integration(self):
        """Test data flow through the entire system"""
        # Test data flow: API -> Tools -> Analysis -> Response
        
        # Step 1: Get player data
        player_stats = get_player_stats("Virat Kohli")
        player_data = json.loads(player_stats)
        assert "player_name" in player_data
        assert "recent_form" in player_data
        assert player_data["player_name"] == "Virat Kohli"
        
        # Step 2: Analyze weaknesses
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        assert "player_name" in weakness_data
        assert "key_weaknesses" in weakness_data
        assert weakness_data["player_name"] == "Virat Kohli"
        
        # Step 3: Generate bowling plan
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        bowling_data = json.loads(bowling_plan)
        assert "player_name" in bowling_data
        assert "overall_strategy" in bowling_data
        assert bowling_data["player_name"] == "Virat Kohli"
        
        # Step 4: Generate fielding plan
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        fielding_data = json.loads(fielding_plan)
        assert "player_name" in fielding_data
        assert "overall_approach" in fielding_data
        assert fielding_data["player_name"] == "Virat Kohli"
        
        # Step 5: Verify data consistency
        assert player_data["player_name"] == weakness_data["player_name"]
        assert player_data["player_name"] == bowling_data["player_name"]
        assert player_data["player_name"] == fielding_data["player_name"]
    
    def test_error_propagation_integration(self):
        """Test error propagation through the system"""
        # Test with invalid player name
        invalid_player_stats = get_player_stats("")
        invalid_data = json.loads(invalid_player_stats)
        assert "error" in invalid_data
        
        # Test weakness analysis with invalid data
        invalid_analysis = analyze_weaknesses("invalid json")
        invalid_analysis_data = json.loads(invalid_analysis)
        assert "error" in invalid_analysis_data
        
        # Test matchup analysis with invalid data
        invalid_matchup = find_best_matchup("invalid json", "invalid json")
        invalid_matchup_data = json.loads(invalid_matchup)
        assert "error" in invalid_matchup_data
    
    def test_unicode_integration(self, test_client):
        """Test unicode handling throughout the system"""
        unicode_query = "Analyze Virat Kohli's batting weaknesses 分析"
        unicode_context = {
            "team": "India 印度",
            "opponent": "Australia 澳大利亚",
            "venue": "Narendra Modi Stadium 纳伦德拉·莫迪体育场"
        }
        
        # Test with unicode data
        player_stats = get_player_stats("Virat Kohli 维拉特·科利")
        player_data = json.loads(player_stats)
        assert "player_name" in player_data
        assert player_data["player_name"] == "Virat Kohli 维拉特·科利"
        
        # Test weakness analysis with unicode
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        assert "player_name" in weakness_data
        assert weakness_data["player_name"] == "Virat Kohli 维拉特·科利"
        
        # Test backend with unicode
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Unicode analysis response",
                "analysis": {},
                "sources": []
            })
            
            request_data = {
                "query": unicode_query,
                "context": unicode_context
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
    
    def test_special_characters_integration(self, test_client):
        """Test special characters handling throughout the system"""
        special_query = "Analyze Virat Kohli's batting weaknesses!@#$%^&*()"
        special_context = {
            "team": "India!@#$%^&*()",
            "opponent": "Australia!@#$%^&*()",
            "venue": "Narendra Modi Stadium!@#$%^&*()"
        }
        
        # Test with special characters
        player_stats = get_player_stats("Virat Kohli!@#$%^&*()")
        player_data = json.loads(player_stats)
        assert "player_name" in player_data
        assert player_data["player_name"] == "Virat Kohli!@#$%^&*()"
        
        # Test weakness analysis with special characters
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        assert "player_name" in weakness_data
        assert weakness_data["player_name"] == "Virat Kohli!@#$%^&*()"
        
        # Test backend with special characters
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Special characters analysis response",
                "analysis": {},
                "sources": []
            })
            
            request_data = {
                "query": special_query,
                "context": special_context
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
    
    def test_large_data_integration(self, test_client):
        """Test large data handling throughout the system"""
        # Test with large context
        large_context = {
            "team": "India",
            "players": [f"Player {i}" for i in range(100)],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {
                    "pitch": "batting_friendly",
                    "weather": "clear"
                }
            },
            "data": {f"key_{i}": f"value_{i}" for i in range(1000)}
        }
        
        # Test backend with large context
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Large data analysis response",
                "analysis": {},
                "sources": []
            })
            
            request_data = {
                "query": "Test query",
                "context": large_context
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
    
    def test_concurrent_requests_integration(self, test_client):
        """Test concurrent requests handling"""
        import threading
        import time
        
        results = []
        
        def make_request():
            with patch('backend.main.agent') as mock_agent:
                mock_agent.analyze = AsyncMock(return_value={
                    "response": f"Response {threading.current_thread().ident}",
                    "analysis": {},
                    "sources": []
                })
                
                request_data = {
                    "query": f"Test query {threading.current_thread().ident}",
                    "context": {"team": "India"}
                }
                
                response = test_client.post("/analyze", json=request_data)
                results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == 5
        for status_code in results:
            assert status_code == 200
    
    def test_memory_usage_integration(self):
        """Test memory usage with large data sets"""
        # Test with large player data
        large_player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0},
            "weaknesses": {f"weakness_{i}": {"average": i} for i in range(1000)},
            "strengths": {f"strength_{i}": {"average": i} for i in range(1000)},
            "recent_matches": [{"runs": i, "balls": i*2} for i in range(1000)]
        }
        
        # Test weakness analysis with large data
        weakness_analysis = analyze_weaknesses(json.dumps(large_player_data))
        weakness_data = json.loads(weakness_analysis)
        assert "player_name" in weakness_data
        assert "key_weaknesses" in weakness_data
        
        # Test bowling plan with large data
        bowling_plan = generate_bowling_plan(json.dumps(large_player_data), "Test context")
        bowling_data = json.loads(bowling_plan)
        assert "player_name" in bowling_data
        assert "overall_strategy" in bowling_data
    
    def test_data_validation_integration(self, test_client):
        """Test data validation throughout the system"""
        # Test with various data types
        test_cases = [
            {"query": "Test query", "context": {"team": "India"}},
            {"query": "Test query", "context": {"team": "India", "players": ["Virat Kohli"]}},
            {"query": "Test query", "context": {"team": "India", "nested": {"key": "value"}}},
            {"query": "Test query", "context": None},
            {"query": "Test query", "context": {}},
        ]
        
        for test_case in test_cases:
            with patch('backend.main.agent') as mock_agent:
                mock_agent.analyze = AsyncMock(return_value={
                    "response": "Test response",
                    "analysis": {},
                    "sources": []
                })
                
                response = test_client.post("/analyze", json=test_case)
                assert response.status_code == 200
                data = response.json()
                assert "response" in data
    
    def test_performance_integration(self):
        """Test performance with multiple operations"""
        import time
        
        start_time = time.time()
        
        # Perform multiple operations
        for i in range(10):
            # Get player stats
            player_stats = get_player_stats(f"Player {i}")
            player_data = json.loads(player_stats)
            assert "player_name" in player_data
            
            # Analyze weaknesses
            weakness_analysis = analyze_weaknesses(player_stats)
            weakness_data = json.loads(weakness_analysis)
            assert "player_name" in weakness_data
            
            # Generate bowling plan
            bowling_plan = generate_bowling_plan(player_stats, f"Context {i}")
            bowling_data = json.loads(bowling_plan)
            assert "player_name" in bowling_data
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify performance is reasonable (should complete within 10 seconds)
        assert execution_time < 10.0
        print(f"Performance test completed in {execution_time:.2f} seconds")


class TestEndToEndScenarios:
    """Test end-to-end scenarios"""
    
    def test_coach_analysis_scenario(self, test_client):
        """Test complete coach analysis scenario"""
        # Scenario: Coach wants to analyze a specific player's weaknesses
        query = "Analyze Virat Kohli's batting weaknesses against spin bowling"
        context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "ODI"
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Virat Kohli shows vulnerability against spin bowling in early overs. Recommend using spinners in the first 10 overs to exploit this weakness.",
                "analysis": {
                    "player_name": "Virat Kohli",
                    "weaknesses": ["against_spin", "early_innings"],
                    "recommendations": ["Use spin bowling", "Attack early"]
                },
                "sources": ["CricAPI", "Historical Data", "Tactical Analysis"]
            })
            
            request_data = {
                "query": query,
                "context": context
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert "spin bowling" in data["response"]
            assert data["analysis"]["player_name"] == "Virat Kohli"
    
    def test_team_analysis_scenario(self, test_client):
        """Test complete team analysis scenario"""
        # Scenario: Coach wants to analyze team strengths and weaknesses
        query = "Analyze India's batting lineup strengths and weaknesses"
        context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "Test"
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "India's batting lineup shows strong top order with Rohit Sharma and Virat Kohli, but middle order needs improvement. Recommend strengthening the middle order batting.",
                "analysis": {
                    "team": "India",
                    "strengths": ["Strong top order", "Experienced players"],
                    "weaknesses": ["Middle order inconsistency", "Lower order batting"],
                    "recommendations": ["Strengthen middle order", "Improve lower order batting"]
                },
                "sources": ["CricAPI", "Team Statistics", "Historical Performance"]
            })
            
            request_data = {
                "query": query,
                "context": context
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert "India" in data["response"]
            assert "batting lineup" in data["response"]
    
    def test_venue_analysis_scenario(self, test_client):
        """Test complete venue analysis scenario"""
        # Scenario: Coach wants to analyze venue conditions
        query = "Analyze Narendra Modi Stadium pitch conditions and batting strategy"
        context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "T20"
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Narendra Modi Stadium offers batting-friendly conditions with good bounce. Recommend aggressive batting approach in powerplay overs.",
                "analysis": {
                    "venue": "Narendra Modi Stadium",
                    "pitch_conditions": "Batting friendly",
                    "recommendations": ["Aggressive batting", "Powerplay focus"],
                    "weather_impact": "Clear skies, good for batting"
                },
                "sources": ["Venue Statistics", "Weather Data", "Historical Matches"]
            })
            
            request_data = {
                "query": query,
                "context": context
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert "Narendra Modi Stadium" in data["response"]
            assert "batting" in data["response"]
    
    def test_matchup_analysis_scenario(self, test_client):
        """Test complete matchup analysis scenario"""
        # Scenario: Coach wants to analyze head-to-head matchup
        query = "Analyze India vs Australia head-to-head record and key matchups"
        context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "ODI"
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "India has a strong record against Australia at home. Key matchups include Virat Kohli vs Pat Cummins and Rohit Sharma vs Mitchell Starc.",
                "analysis": {
                    "head_to_head": "India leads 3-2",
                    "key_matchups": ["Virat Kohli vs Pat Cummins", "Rohit Sharma vs Mitchell Starc"],
                    "recommendations": ["Focus on key matchups", "Exploit home advantage"]
                },
                "sources": ["Head-to-Head Records", "Player Statistics", "Venue History"]
            })
            
            request_data = {
                "query": query,
                "context": context
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert "India" in data["response"]
            assert "Australia" in data["response"]
    
    def test_tactical_planning_scenario(self, test_client):
        """Test complete tactical planning scenario"""
        # Scenario: Coach wants to create a tactical plan
        query = "Create a tactical plan for India's bowling against Australia's top order"
        context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium",
            "match_type": "ODI",
            "focus": "bowling"
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Tactical plan: Use Jasprit Bumrah and Mohammed Shami in powerplay overs to target Australia's openers. Use spinners in middle overs to build pressure.",
                "analysis": {
                    "bowling_plan": {
                        "powerplay": "Use pace bowlers",
                        "middle_overs": "Use spinners",
                        "death_overs": "Use specialist death bowlers"
                    },
                    "field_placements": ["Attacking field in powerplay", "Balanced field in middle overs"],
                    "key_bowlers": ["Jasprit Bumrah", "Mohammed Shami", "Ravindra Jadeja"]
                },
                "sources": ["Player Statistics", "Tactical Analysis", "Venue Conditions"]
            })
            
            request_data = {
                "query": query,
                "context": context
            }
            
            response = test_client.post("/analyze", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "analysis" in data
            assert "sources" in data
            assert "bowling" in data["response"]
            assert "tactical plan" in data["response"]


class TestSystemReliability:
    """Test system reliability scenarios"""
    
    def test_system_under_load(self, test_client):
        """Test system performance under load"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                with patch('backend.main.agent') as mock_agent:
                    mock_agent.analyze = AsyncMock(return_value={
                        "response": "Test response",
                        "analysis": {},
                        "sources": []
                    })
                    
                    request_data = {
                        "query": f"Test query {threading.current_thread().ident}",
                        "context": {"team": "India"}
                    }
                    
                    response = test_client.post("/analyze", json=request_data)
                    results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads for load testing
        threads = []
        for i in range(20):  # Increased load
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify system handled the load
        assert len(results) == 20
        assert len(errors) == 0
        for status_code in results:
            assert status_code == 200
    
    def test_system_error_recovery(self, test_client):
        """Test system error recovery"""
        # Test with agent unavailable
        with patch('backend.main.agent', None):
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 503
        
        # Test with agent throwing exception
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(side_effect=Exception("Test error"))
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 500
        
        # Test system recovery after errors
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Recovery response",
                "analysis": {},
                "sources": []
            })
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["response"] == "Recovery response"
    
    def test_system_data_consistency(self):
        """Test system data consistency across components"""
        # Test that data flows consistently through the system
        player_name = "Virat Kohli"
        
        # Get player stats
        player_stats = get_player_stats(player_name)
        player_data = json.loads(player_stats)
        original_name = player_data["player_name"]
        
        # Analyze weaknesses
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        weakness_name = weakness_data["player_name"]
        
        # Generate bowling plan
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        bowling_data = json.loads(bowling_plan)
        bowling_name = bowling_data["player_name"]
        
        # Generate fielding plan
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        fielding_data = json.loads(fielding_plan)
        fielding_name = fielding_data["player_name"]
        
        # Verify data consistency
        assert original_name == weakness_name
        assert original_name == bowling_name
        assert original_name == fielding_name
        assert original_name == player_name
    
    def test_system_unicode_handling(self, test_client):
        """Test system unicode handling"""
        unicode_test_cases = [
            "Analyze Virat Kohli's batting 分析",
            "Test query 测试查询",
            "Cricket analysis 板球分析",
            "Tactical planning 战术规划"
        ]
        
        for unicode_query in unicode_test_cases:
            with patch('backend.main.agent') as mock_agent:
                mock_agent.analyze = AsyncMock(return_value={
                    "response": f"Unicode response for {unicode_query}",
                    "analysis": {},
                    "sources": []
                })
                
                request_data = {
                    "query": unicode_query,
                    "context": {"team": "India 印度"}
                }
                
                response = test_client.post("/analyze", json=request_data)
                assert response.status_code == 200
                data = response.json()
                assert "response" in data
                assert unicode_query in data["response"]
    
    def test_system_special_characters_handling(self, test_client):
        """Test system special characters handling"""
        special_test_cases = [
            "Analyze Virat Kohli's batting!@#$%^&*()",
            "Test query!@#$%^&*()",
            "Cricket analysis!@#$%^&*()",
            "Tactical planning!@#$%^&*()"
        ]
        
        for special_query in special_test_cases:
            with patch('backend.main.agent') as mock_agent:
                mock_agent.analyze = AsyncMock(return_value={
                    "response": f"Special response for {special_query}",
                    "analysis": {},
                    "sources": []
                })
                
                request_data = {
                    "query": special_query,
                    "context": {"team": "India!@#$%^&*()"}
                }
                
                response = test_client.post("/analyze", json=request_data)
                assert response.status_code == 200
                data = response.json()
                assert "response" in data
                assert special_query in data["response"]
