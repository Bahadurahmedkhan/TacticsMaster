"""
Comprehensive Error Handling Tests for Tactics Master System

This module contains comprehensive error handling tests for all components
including network failures, invalid data, and edge cases.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import os
import sys
import requests
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

class TestNetworkErrorHandling(unittest.TestCase):
    """Test network error handling scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Test query"
        self.sample_context = {"team": "India"}
    
    @patch('backend.main.agent')
    def test_network_timeout_error(self, mock_agent):
        """Test network timeout error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.Timeout("Request timeout"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("timeout", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_connection_error(self, mock_agent):
        """Test network connection error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.ConnectionError("Connection failed"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Connection failed", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_http_error(self, mock_agent):
        """Test HTTP error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.HTTPError("HTTP error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("HTTP error", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_request_exception(self, mock_agent):
        """Test request exception handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.RequestException("Request exception"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Request exception", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_ssl_error(self, mock_agent):
        """Test SSL error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.exceptions.SSLError("SSL error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("SSL error", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_proxy_error(self, mock_agent):
        """Test proxy error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.exceptions.ProxyError("Proxy error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Proxy error", data["detail"])
    
    @patch('backend.main.agent')
    def test_network_retry_error(self, mock_agent):
        """Test retry error handling"""
        mock_agent.analyze = AsyncMock(side_effect=requests.exceptions.RetryError("Retry error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Retry error", data["detail"])

class TestDataValidationErrorHandling(unittest.TestCase):
    """Test data validation error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_invalid_json_request(self):
        """Test invalid JSON request handling"""
        response = self.client.post(
            "/analyze",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 422)
    
    def test_missing_required_fields(self):
        """Test missing required fields handling"""
        request_data = {
            "context": {"team": "India"}
            # Missing 'query' field
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_invalid_field_types(self):
        """Test invalid field types handling"""
        request_data = {
            "query": 123,  # Should be string
            "context": "invalid"  # Should be dict
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_field_length_validation(self):
        """Test field length validation"""
        # Test query too long
        request_data = {
            "query": "A" * 1001,  # Exceeds max_length of 1000
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_empty_required_fields(self):
        """Test empty required fields handling"""
        request_data = {
            "query": "",  # Empty string
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_whitespace_only_fields(self):
        """Test whitespace-only fields handling"""
        request_data = {
            "query": "   ",  # Only whitespace
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_none_values(self):
        """Test None values handling"""
        request_data = {
            "query": None,  # None value
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_invalid_context_structure(self):
        """Test invalid context structure handling"""
        request_data = {
            "query": "Test query",
            "context": "invalid context"  # Should be dict
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_circular_reference_context(self):
        """Test circular reference in context handling"""
        # Create circular reference
        circular_context = {"key": "value"}
        circular_context["self"] = circular_context
        
        request_data = {
            "query": "Test query",
            "context": circular_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle circular reference gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_very_deep_nested_context(self):
        """Test very deep nested context handling"""
        # Create deeply nested context
        nested_context = {"level1": {"level2": {"level3": {"level4": {"level5": {"value": "deep"}}}}}
        
        request_data = {
            "query": "Test query",
            "context": nested_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle deep nesting gracefully
        self.assertIn(response.status_code, [200, 422])

class TestCricketApiToolsErrorHandling(unittest.TestCase):
    """Test cricket API tools error handling"""
    
    def test_get_player_stats_network_error(self):
        """Test get_player_stats network error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network error")
            
            result = get_player_stats("Virat Kohli")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_get_player_stats_timeout_error(self):
        """Test get_player_stats timeout error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.Timeout("Request timeout")
            
            result = get_player_stats("Virat Kohli")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_get_player_stats_http_error(self):
        """Test get_player_stats HTTP error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.HTTPError("HTTP error")
            
            result = get_player_stats("Virat Kohli")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_get_team_squad_network_error(self):
        """Test get_team_squad network error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network error")
            
            result = get_team_squad("India")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_get_matchup_data_network_error(self):
        """Test get_matchup_data network error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network error")
            
            result = get_matchup_data("India", "Australia")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_get_venue_stats_network_error(self):
        """Test get_venue_stats network error handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network error")
            
            result = get_venue_stats("Narendra Modi Stadium")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_cricket_api_tools_malformed_response(self):
        """Test cricket API tools malformed response handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)
            mock_get.return_value = mock_response
            
            result = get_player_stats("Virat Kohli")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)
    
    def test_cricket_api_tools_invalid_status_code(self):
        """Test cricket API tools invalid status code handling"""
        with patch('app.tools.cricket_api_tools.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.json.return_value = {"error": "Internal server error"}
            mock_get.return_value = mock_response
            
            result = get_player_stats("Virat Kohli")
            
            # Should return error JSON instead of crashing
            data = json.loads(result)
            self.assertIn("error", data)

class TestTacticalToolsErrorHandling(unittest.TestCase):
    """Test tactical tools error handling"""
    
    def test_analyze_weaknesses_invalid_json(self):
        """Test analyze_weaknesses invalid JSON handling"""
        result = analyze_weaknesses("invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_empty_data(self):
        """Test analyze_weaknesses empty data handling"""
        result = analyze_weaknesses("")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_none_data(self):
        """Test analyze_weaknesses None data handling"""
        result = analyze_weaknesses(None)
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_analyze_weaknesses_malformed_data(self):
        """Test analyze_weaknesses malformed data handling"""
        malformed_data = {"player_name": "Test", "invalid_field": "value"}
        result = analyze_weaknesses(json.dumps(malformed_data))
        
        data = json.loads(result)
        self.assertIn("player_name", data)
        self.assertIn("overall_assessment", data)
    
    def test_find_best_matchup_invalid_data(self):
        """Test find_best_matchup invalid data handling"""
        result = find_best_matchup("invalid json", "invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_find_best_matchup_empty_data(self):
        """Test find_best_matchup empty data handling"""
        result = find_best_matchup("", "")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_find_best_matchup_none_data(self):
        """Test find_best_matchup None data handling"""
        result = find_best_matchup(None, None)
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_bowling_plan_invalid_data(self):
        """Test generate_bowling_plan invalid data handling"""
        result = generate_bowling_plan("invalid json", "Test context")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_bowling_plan_empty_context(self):
        """Test generate_bowling_plan empty context handling"""
        player_data = {"player_name": "Test Player", "recent_form": {"batting_average": 45.0}}
        result = generate_bowling_plan(json.dumps(player_data), "")
        
        data = json.loads(result)
        self.assertEqual(data["context"], "")
        self.assertIn("overall_strategy", data)
    
    def test_generate_bowling_plan_none_context(self):
        """Test generate_bowling_plan None context handling"""
        player_data = {"player_name": "Test Player", "recent_form": {"batting_average": 45.0}}
        result = generate_bowling_plan(json.dumps(player_data), None)
        
        data = json.loads(result)
        self.assertIsNone(data["context"])
        self.assertIn("overall_strategy", data)
    
    def test_generate_fielding_plan_invalid_data(self):
        """Test generate_fielding_plan invalid data handling"""
        result = generate_fielding_plan("invalid json", "invalid json")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_fielding_plan_empty_bowling_plan(self):
        """Test generate_fielding_plan empty bowling plan handling"""
        player_data = {"player_name": "Test Player", "recent_form": {"batting_average": 45.0}}
        result = generate_fielding_plan(json.dumps(player_data), "")
        
        data = json.loads(result)
        self.assertIn("error", data)
    
    def test_generate_fielding_plan_none_bowling_plan(self):
        """Test generate_fielding_plan None bowling plan handling"""
        player_data = {"player_name": "Test Player", "recent_form": {"batting_average": 45.0}}
        result = generate_fielding_plan(json.dumps(player_data), None)
        
        data = json.loads(result)
        self.assertIn("error", data)

class TestAgentErrorHandling(unittest.TestCase):
    """Test agent error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_llm = Mock()
        self.mock_tools = [Mock(), Mock()]
        self.mock_tools[0].name = "test_tool_1"
        self.mock_tools[1].name = "test_tool_2"
    
    def test_agent_initialization_llm_none(self):
        """Test agent initialization with None LLM"""
        with self.assertRaises(ValueError):
            TacticsMasterAgent(None, self.mock_tools)
    
    def test_agent_initialization_empty_tools(self):
        """Test agent initialization with empty tools"""
        with self.assertRaises(ValueError):
            TacticsMasterAgent(self.mock_llm, [])
    
    def test_agent_initialization_none_tools(self):
        """Test agent initialization with None tools"""
        with self.assertRaises(ValueError):
            TacticsMasterAgent(self.mock_llm, None)
    
    def test_agent_analyze_empty_query(self):
        """Test agent analyze with empty query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze("")
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    def test_agent_analyze_none_query(self):
        """Test agent analyze with None query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze(None)
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    def test_agent_analyze_whitespace_query(self):
        """Test agent analyze with whitespace-only query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze("   ")
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    @patch('app.agent.AgentExecutor')
    def test_agent_analyze_exception(self, mock_agent_executor_class):
        """Test agent analyze exception handling"""
        # Setup mock agent executor to raise exception
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("Analysis failed")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        agent.agent_executor = mock_executor
        
        result = agent.analyze("Test query")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    def test_agent_get_available_tools_exception(self):
        """Test agent get_available_tools exception handling"""
        # Create agent with tools that raise exception when accessing name
        mock_tool = Mock()
        mock_tool.name = Mock(side_effect=Exception("Tool name error"))
        agent = TacticsMasterAgent(self.mock_llm, [mock_tool])
        
        tools = agent.get_available_tools()
        
        self.assertEqual(tools, [])
    
    def test_agent_get_agent_info_exception(self):
        """Test agent get_agent_info exception handling"""
        # Create agent with tools that raise exception
        mock_tool = Mock()
        mock_tool.name = Mock(side_effect=Exception("Tool error"))
        agent = TacticsMasterAgent(self.mock_llm, [mock_tool])
        
        info = agent.get_agent_info()
        
        self.assertEqual(info["name"], "Tactics Master")
        self.assertEqual(info["version"], "1.0.0")
        self.assertEqual(info["available_tools"], [])
        self.assertEqual(info["tools_count"], 0)
        self.assertFalse(info["verbose"])

class TestBackendErrorHandling(unittest.TestCase):
    """Test backend error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_backend_agent_unavailable(self):
        """Test backend when agent is unavailable"""
        with patch('backend.main.agent', None):
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("unavailable", data["detail"])
    
    def test_backend_agent_exception(self):
        """Test backend when agent raises exception"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(side_effect=Exception("Agent error"))
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("Agent error", data["detail"])
    
    def test_backend_invalid_request(self):
        """Test backend with invalid request"""
        response = self.client.post("/analyze", json="invalid json")
        
        self.assertEqual(response.status_code, 422)
    
    def test_backend_missing_content_type(self):
        """Test backend without content type"""
        response = self.client.post(
            "/analyze",
            data='{"query": "Test query", "context": {"team": "India"}}'
        )
        
        # Should still work as FastAPI can handle JSON without explicit content type
        self.assertIn(response.status_code, [200, 422])
    
    def test_backend_unsupported_media_type(self):
        """Test backend with unsupported media type"""
        response = self.client.post(
            "/analyze",
            data="Test data",
            headers={"Content-Type": "text/plain"}
        )
        
        self.assertEqual(response.status_code, 422)
    
    def test_backend_request_too_large(self):
        """Test backend with request too large"""
        large_query = "A" * 10000  # Very large query
        request_data = {
            "query": large_query,
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_backend_malformed_json(self):
        """Test backend with malformed JSON"""
        response = self.client.post(
            "/analyze",
            data='{"query": "Test query", "context": {"team": "India"',  # Missing closing brace
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 422)
    
    def test_backend_unicode_error(self):
        """Test backend with unicode error"""
        # Create request with invalid unicode
        invalid_unicode = b'\xff\xfe\x00\x00'  # Invalid UTF-8
        
        response = self.client.post(
            "/analyze",
            data=invalid_unicode,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 422)
    
    def test_backend_memory_error(self):
        """Test backend with memory error"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(side_effect=MemoryError("Memory error"))
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("Memory error", data["detail"])
    
    def test_backend_keyboard_interrupt(self):
        """Test backend with keyboard interrupt"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(side_effect=KeyboardInterrupt("Interrupted"))
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("Interrupted", data["detail"])
    
    def test_backend_system_exit(self):
        """Test backend with system exit"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(side_effect=SystemExit("System exit"))
            
            request_data = {
                "query": "Test query",
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("System exit", data["detail"])

class TestEdgeCaseErrorHandling(unittest.TestCase):
    """Test edge case error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_very_long_query(self):
        """Test very long query handling"""
        long_query = "A" * 10000  # Very long query
        
        request_data = {
            "query": long_query,
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)
    
    def test_very_deep_nested_context(self):
        """Test very deep nested context handling"""
        # Create very deep nested context
        nested_context = {"level1": {"level2": {"level3": {"level4": {"level5": {"level6": {"level7": {"level8": {"level9": {"level10": {"value": "deep"}}}}}}}}}}
        
        request_data = {
            "query": "Test query",
            "context": nested_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle deep nesting gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_circular_reference_context(self):
        """Test circular reference context handling"""
        # Create circular reference
        circular_context = {"key": "value"}
        circular_context["self"] = circular_context
        
        request_data = {
            "query": "Test query",
            "context": circular_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle circular reference gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_unicode_query(self):
        """Test unicode query handling"""
        unicode_query = "Test query 测试 🏏"
        
        request_data = {
            "query": unicode_query,
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle unicode gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_special_characters_query(self):
        """Test special characters query handling"""
        special_query = "Test query!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        request_data = {
            "query": special_query,
            "context": {"team": "India"}
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle special characters gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_mixed_data_types_context(self):
        """Test mixed data types context handling"""
        mixed_context = {
            "string": "India",
            "integer": 123,
            "float": 45.67,
            "boolean": True,
            "list": ["item1", "item2"],
            "dict": {"key": "value"},
            "none": None
        }
        
        request_data = {
            "query": "Test query",
            "context": mixed_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle mixed data types gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_large_context(self):
        """Test large context handling"""
        large_context = {
            "team": "India",
            "players": [f"Player {i}" for i in range(1000)],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {
                    "pitch": "batting_friendly",
                    "weather": "clear"
                }
            },
            "data": {f"key_{i}": f"value_{i}" for i in range(10000)}
        }
        
        request_data = {
            "query": "Test query",
            "context": large_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        # Should handle large context gracefully
        self.assertIn(response.status_code, [200, 422])
    
    def test_concurrent_requests(self):
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
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        self.assertEqual(len(results), 10)
        for status_code in results:
            self.assertEqual(status_code, 200)

if __name__ == '__main__':
    unittest.main()
