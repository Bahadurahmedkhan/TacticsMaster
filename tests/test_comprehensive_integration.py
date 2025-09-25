"""
Comprehensive Integration Tests for Tactics Master System

This module contains comprehensive integration tests that test the complete workflow
from API calls to response generation, including end-to-end scenarios.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import os
import sys
import asyncio
from typing import Dict, Any, List
from fastapi.testclient import TestClient

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Mock the hybrid_agent import before importing main
with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
    from main import app

from agent import TacticsMasterAgent
from tools.cricket_api_tools import get_player_stats, get_team_squad, get_matchup_data, get_venue_stats
from tools.tactical_tools import analyze_weaknesses, find_best_matchup, generate_bowling_plan, generate_fielding_plan

class TestCompleteWorkflowIntegration(unittest.TestCase):
    """Test complete workflow integration scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Analyze Virat Kohli's batting weaknesses against Australia"
        self.sample_context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium"
        }
        
        # Mock agent response
        self.mock_agent_response = {
            "response": "Comprehensive analysis of Virat Kohli's batting weaknesses",
            "analysis": {
                "player_name": "Virat Kohli",
                "weaknesses": ["against_spin", "early_innings"],
                "recommendations": ["Use spin bowling", "Attack early"]
            },
            "sources": ["CricAPI", "Historical Data", "Tactical Analysis"]
        }
    
    @patch('backend.main.agent')
    def test_complete_analysis_workflow(self, mock_agent):
        """Test complete analysis workflow from API to response"""
        # Setup mock agent
        mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
        
        # Test the complete workflow
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("analysis", data)
        self.assertIn("sources", data)
        
        # Verify agent was called with correct parameters
        mock_agent.analyze.assert_called_once_with(
            self.sample_query,
            self.sample_context
        )
    
    def test_cricket_api_tools_integration(self):
        """Test integration between cricket API tools"""
        # Test player stats
        player_stats = get_player_stats("Virat Kohli")
        self.assertIsInstance(player_stats, str)
        player_data = json.loads(player_stats)
        self.assertIn("player_name", player_data)
        self.assertIn("recent_form", player_data)
        
        # Test team squad
        team_squad = get_team_squad("India")
        self.assertIsInstance(team_squad, str)
        team_data = json.loads(team_squad)
        self.assertIn("team_name", team_data)
        self.assertIn("squad", team_data)
        
        # Test matchup data
        matchup_data = get_matchup_data("India", "Australia")
        self.assertIsInstance(matchup_data, str)
        matchup_result = json.loads(matchup_data)
        self.assertIn("head_to_head", matchup_result)
        self.assertIn("recent_encounters", matchup_result)
        
        # Test venue stats
        venue_stats = get_venue_stats("Narendra Modi Stadium")
        self.assertIsInstance(venue_stats, str)
        venue_data = json.loads(venue_stats)
        self.assertIn("venue_name", venue_data)
        self.assertIn("pitch_conditions", venue_data)
    
    def test_tactical_tools_integration(self):
        """Test integration between tactical analysis tools"""
        # Get player data
        player_stats = get_player_stats("Virat Kohli")
        player_data = json.loads(player_stats)
        
        # Test weakness analysis
        weakness_analysis = analyze_weaknesses(player_stats)
        self.assertIsInstance(weakness_analysis, str)
        weakness_data = json.loads(weakness_analysis)
        self.assertIn("player_name", weakness_data)
        self.assertIn("key_weaknesses", weakness_data)
        self.assertIn("recommendations", weakness_data)
        
        # Test matchup analysis
        player2_stats = get_player_stats("Rohit Sharma")
        matchup_analysis = find_best_matchup(player_stats, player2_stats)
        self.assertIsInstance(matchup_analysis, str)
        matchup_data = json.loads(matchup_analysis)
        self.assertIn("player1", matchup_data)
        self.assertIn("player2", matchup_data)
        self.assertIn("matchup_assessment", matchup_data)
        
        # Test bowling plan generation
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        self.assertIsInstance(bowling_plan, str)
        bowling_data = json.loads(bowling_plan)
        self.assertIn("player_name", bowling_data)
        self.assertIn("overall_strategy", bowling_data)
        self.assertIn("phase_plans", bowling_data)
        
        # Test fielding plan generation
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        self.assertIsInstance(fielding_plan, str)
        fielding_data = json.loads(fielding_plan)
        self.assertIn("player_name", fielding_data)
        self.assertIn("overall_approach", fielding_data)
        self.assertIn("phase_fielding", fielding_data)
    
    def test_agent_tools_integration(self):
        """Test integration between agent and tools"""
        # Mock LLM and tools
        mock_llm = Mock()
        mock_tools = [Mock(), Mock(), Mock(), Mock()]
        mock_tools[0].name = "get_player_stats"
        mock_tools[1].name = "get_team_squad"
        mock_tools[2].name = "analyze_weaknesses"
        mock_tools[3].name = "generate_bowling_plan"
        
        # Create agent
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Test agent initialization
        self.assertEqual(agent.llm, mock_llm)
        self.assertEqual(agent.tools, mock_tools)
        self.assertTrue(agent.verbose)
        
        # Test agent info
        info = agent.get_agent_info()
        self.assertEqual(info["name"], "Tactics Master")
        self.assertEqual(info["version"], "1.0.0")
        self.assertIn("cricket", info["description"].lower())
        self.assertEqual(info["available_tools"], ["get_player_stats", "get_team_squad", "analyze_weaknesses", "generate_bowling_plan"])
    
    def test_backend_health_integration(self):
        """Test backend health integration"""
        # Test health endpoint
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("agent_available", data)
        self.assertIn("timestamp", data)
    
    def test_backend_root_integration(self):
        """Test backend root endpoint integration"""
        # Test root endpoint
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
        self.assertIn("docs", data)
        self.assertEqual(data["version"], "1.0.0")
    
    def test_data_flow_integration(self):
        """Test data flow through the entire system"""
        # Test data flow: API -> Tools -> Analysis -> Response
        
        # Step 1: Get player data
        player_stats = get_player_stats("Virat Kohli")
        player_data = json.loads(player_stats)
        self.assertIn("player_name", player_data)
        self.assertIn("recent_form", player_data)
        
        # Step 2: Analyze weaknesses
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        self.assertIn("player_name", weakness_data)
        self.assertIn("key_weaknesses", weakness_data)
        
        # Step 3: Generate bowling plan
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        bowling_data = json.loads(bowling_plan)
        self.assertIn("player_name", bowling_data)
        self.assertIn("overall_strategy", bowling_data)
        
        # Step 4: Generate fielding plan
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        fielding_data = json.loads(fielding_plan)
        self.assertIn("player_name", fielding_data)
        self.assertIn("overall_approach", fielding_data)
        
        # Step 5: Verify data consistency
        self.assertEqual(player_data["player_name"], weakness_data["player_name"])
        self.assertEqual(player_data["player_name"], bowling_data["player_name"])
        self.assertEqual(player_data["player_name"], fielding_data["player_name"])
    
    def test_error_propagation_integration(self):
        """Test error propagation through the system"""
        # Test with invalid player name
        invalid_player_stats = get_player_stats("")
        invalid_data = json.loads(invalid_player_stats)
        self.assertIn("error", invalid_data)
        
        # Test weakness analysis with invalid data
        invalid_analysis = analyze_weaknesses("invalid json")
        invalid_analysis_data = json.loads(invalid_analysis)
        self.assertIn("error", invalid_analysis_data)
        
        # Test matchup analysis with invalid data
        invalid_matchup = find_best_matchup("invalid json", "invalid json")
        invalid_matchup_data = json.loads(invalid_matchup)
        self.assertIn("error", invalid_matchup_data)
    
    def test_unicode_integration(self):
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
        self.assertIn("player_name", player_data)
        
        # Test weakness analysis with unicode
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        self.assertIn("player_name", weakness_data)
        
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
            
            response = self.client.post("/analyze", json=request_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
    
    def test_special_characters_integration(self):
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
        self.assertIn("player_name", player_data)
        
        # Test weakness analysis with special characters
        weakness_analysis = analyze_weaknesses(player_stats)
        weakness_data = json.loads(weakness_analysis)
        self.assertIn("player_name", weakness_data)
        
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
            
            response = self.client.post("/analyze", json=request_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
    
    def test_large_data_integration(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
    
    def test_concurrent_requests_integration(self):
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
                
                response = self.client.post("/analyze", json=request_data)
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
        self.assertEqual(len(results), 5)
        for status_code in results:
            self.assertEqual(status_code, 200)
    
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
        self.assertIn("player_name", weakness_data)
        self.assertIn("key_weaknesses", weakness_data)
        
        # Test bowling plan with large data
        bowling_plan = generate_bowling_plan(json.dumps(large_player_data), "Test context")
        bowling_data = json.loads(bowling_plan)
        self.assertIn("player_name", bowling_data)
        self.assertIn("overall_strategy", bowling_data)
    
    def test_data_validation_integration(self):
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
                
                response = self.client.post("/analyze", json=test_case)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn("response", data)
    
    def test_performance_integration(self):
        """Test performance with multiple operations"""
        import time
        
        start_time = time.time()
        
        # Perform multiple operations
        for i in range(10):
            # Get player stats
            player_stats = get_player_stats(f"Player {i}")
            player_data = json.loads(player_stats)
            self.assertIn("player_name", player_data)
            
            # Analyze weaknesses
            weakness_analysis = analyze_weaknesses(player_stats)
            weakness_data = json.loads(weakness_analysis)
            self.assertIn("player_name", weakness_data)
            
            # Generate bowling plan
            bowling_plan = generate_bowling_plan(player_stats, f"Context {i}")
            bowling_data = json.loads(bowling_plan)
            self.assertIn("player_name", bowling_data)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify performance is reasonable (should complete within 10 seconds)
        self.assertLess(execution_time, 10.0)
        print(f"Performance test completed in {execution_time:.2f} seconds")

class TestEndToEndScenarios(unittest.TestCase):
    """Test end-to-end scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_coach_analysis_scenario(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            self.assertIn("analysis", data)
            self.assertIn("sources", data)
            self.assertIn("spin bowling", data["response"])
            self.assertIn("Virat Kohli", data["analysis"]["player_name"])
    
    def test_team_analysis_scenario(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            self.assertIn("analysis", data)
            self.assertIn("sources", data)
            self.assertIn("India", data["response"])
            self.assertIn("batting lineup", data["response"])
    
    def test_venue_analysis_scenario(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            self.assertIn("analysis", data)
            self.assertIn("sources", data)
            self.assertIn("Narendra Modi Stadium", data["response"])
            self.assertIn("batting", data["response"])
    
    def test_matchup_analysis_scenario(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            self.assertIn("analysis", data)
            self.assertIn("sources", data)
            self.assertIn("India", data["response"])
            self.assertIn("Australia", data["response"])
    
    def test_tactical_planning_scenario(self):
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
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            self.assertIn("analysis", data)
            self.assertIn("sources", data)
            self.assertIn("bowling", data["response"])
            self.assertIn("tactical plan", data["response"])

if __name__ == '__main__':
    unittest.main()
