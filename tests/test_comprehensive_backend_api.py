"""
Comprehensive Unit Tests for FastAPI Backend

This module contains comprehensive unit tests for the FastAPI backend endpoints
including /analyze, /health, and error handling scenarios.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import os
import sys
from typing import Dict, Any, List
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Mock the hybrid_agent import before importing main
with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
    from main import app, QueryRequest, QueryResponse, HealthResponse

class TestBackendApiComprehensive(unittest.TestCase):
    """Comprehensive test cases for FastAPI backend"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Analyze Virat Kohli's batting weaknesses"
        self.sample_context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium"
        }
        
        # Mock agent response
        self.mock_agent_response = {
            "response": "Test analysis response",
            "analysis": {
                "player_name": "Virat Kohli",
                "weaknesses": ["against_spin", "early_innings"]
            },
            "sources": ["CricAPI", "Historical Data"]
        }
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
        self.assertIn("docs", data)
        self.assertEqual(data["version"], "1.0.0")
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_success(self, mock_agent):
        """Test successful analysis endpoint"""
        # Setup mock agent
        mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("analysis", data)
        self.assertIn("sources", data)
        self.assertEqual(data["response"], "Test analysis response")
        self.assertEqual(data["analysis"]["player_name"], "Virat Kohli")
        self.assertEqual(data["sources"], ["CricAPI", "Historical Data"])
        
        # Verify agent was called with correct parameters
        mock_agent.analyze.assert_called_once_with(
            self.sample_query,
            self.sample_context
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_without_context(self, mock_agent):
        """Test analysis endpoint without context"""
        # Setup mock agent
        mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
        
        request_data = {
            "query": self.sample_query
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("analysis", data)
        self.assertIn("sources", data)
        
        # Verify agent was called with empty context
        mock_agent.analyze.assert_called_once_with(
            self.sample_query,
            {}
        )
    
    @patch('backend.main.agent', None)
    def test_analyze_endpoint_agent_unavailable(self):
        """Test analysis endpoint when agent is unavailable"""
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("unavailable", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_agent_exception(self, mock_agent):
        """Test analysis endpoint when agent raises exception"""
        # Setup mock agent to raise exception
        mock_agent.analyze = AsyncMock(side_effect=Exception("Analysis failed"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Analysis failed", data["detail"])
    
    def test_analyze_endpoint_invalid_request(self):
        """Test analysis endpoint with invalid request"""
        # Test with missing query
        request_data = {
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_endpoint_empty_query(self):
        """Test analysis endpoint with empty query"""
        request_data = {
            "query": "",
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_endpoint_too_long_query(self):
        """Test analysis endpoint with query too long"""
        long_query = "A" * 1001  # Exceeds max_length of 1000
        request_data = {
            "query": long_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_endpoint_invalid_json(self):
        """Test analysis endpoint with invalid JSON"""
        response = self.client.post(
            "/analyze",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 422)
    
    def test_analyze_endpoint_missing_content_type(self):
        """Test analysis endpoint without content type"""
        response = self.client.post(
            "/analyze",
            data=json.dumps({"query": self.sample_query})
        )
        
        # Should still work as FastAPI can handle JSON without explicit content type
        self.assertIn(response.status_code, [200, 422])
    
    def test_health_endpoint_agent_available(self):
        """Test health endpoint when agent is available"""
        with patch('backend.main.agent', Mock()):
            response = self.client.get("/health")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("status", data)
            self.assertIn("agent_available", data)
            self.assertIn("timestamp", data)
            self.assertEqual(data["status"], "healthy")
            self.assertTrue(data["agent_available"])
    
    def test_health_endpoint_agent_unavailable(self):
        """Test health endpoint when agent is unavailable"""
        with patch('backend.main.agent', None):
            response = self.client.get("/health")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("status", data)
            self.assertIn("agent_available", data)
            self.assertIn("timestamp", data)
            self.assertEqual(data["status"], "degraded")
            self.assertFalse(data["agent_available"])
    
    def test_health_endpoint_timestamp_format(self):
        """Test health endpoint timestamp format"""
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("timestamp", data)
        
        # Should be valid ISO format timestamp
        from datetime import datetime
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.options("/analyze")
        
        # Should include CORS headers
        self.assertIn("Access-Control-Allow-Origin", response.headers)
        self.assertIn("Access-Control-Allow-Methods", response.headers)
        self.assertIn("Access-Control-Allow-Headers", response.headers)
    
    def test_analyze_endpoint_with_complex_context(self):
        """Test analysis endpoint with complex context structure"""
        complex_context = {
            "team": "India",
            "players": ["Virat Kohli", "Rohit Sharma"],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {
                    "pitch": "batting_friendly",
                    "weather": "clear"
                }
            },
            "nested": {
                "deep": {
                    "value": "test"
                }
            }
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": self.sample_query,
                "context": complex_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with complex context
            mock_agent.analyze.assert_called_once_with(
                self.sample_query,
                complex_context
            )
    
    def test_analyze_endpoint_with_unicode_query(self):
        """Test analysis endpoint with unicode query"""
        unicode_query = "Analyze Virat Kohli's batting weaknesses 分析"
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": unicode_query,
                "context": self.sample_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with unicode query
            mock_agent.analyze.assert_called_once_with(
                unicode_query,
                self.sample_context
            )
    
    def test_analyze_endpoint_with_special_characters(self):
        """Test analysis endpoint with special characters"""
        special_query = "Analyze Virat Kohli's batting!@#$%^&*()"
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": special_query,
                "context": self.sample_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with special characters
            mock_agent.analyze.assert_called_once_with(
                special_query,
                self.sample_context
            )
    
    def test_analyze_endpoint_with_none_context(self):
        """Test analysis endpoint with None context"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": self.sample_query,
                "context": None
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with None context
            mock_agent.analyze.assert_called_once_with(
                self.sample_query,
                None
            )
    
    def test_analyze_endpoint_with_empty_context(self):
        """Test analysis endpoint with empty context"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": self.sample_query,
                "context": {}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with empty context
            mock_agent.analyze.assert_called_once_with(
                self.sample_query,
                {}
            )
    
    def test_analyze_endpoint_with_large_context(self):
        """Test analysis endpoint with large context"""
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
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value=self.mock_agent_response)
            
            request_data = {
                "query": self.sample_query,
                "context": large_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("response", data)
            
            # Verify agent was called with large context
            mock_agent.analyze.assert_called_once_with(
                self.sample_query,
                large_context
            )

class TestBackendApiErrorHandling(unittest.TestCase):
    """Test error handling scenarios for backend API"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Test query"
        self.sample_context = {"team": "India"}
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_network_timeout(self, mock_agent):
        """Test analysis endpoint with network timeout"""
        # Setup mock agent to raise timeout exception
        mock_agent.analyze = AsyncMock(side_effect=TimeoutError("Request timeout"))
        
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
    def test_analyze_endpoint_connection_error(self, mock_agent):
        """Test analysis endpoint with connection error"""
        # Setup mock agent to raise connection error
        mock_agent.analyze = AsyncMock(side_effect=ConnectionError("Connection failed"))
        
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
    def test_analyze_endpoint_value_error(self, mock_agent):
        """Test analysis endpoint with value error"""
        # Setup mock agent to raise value error
        mock_agent.analyze = AsyncMock(side_effect=ValueError("Invalid value"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Invalid value", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_key_error(self, mock_agent):
        """Test analysis endpoint with key error"""
        # Setup mock agent to raise key error
        mock_agent.analyze = AsyncMock(side_effect=KeyError("Missing key"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Missing key", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_type_error(self, mock_agent):
        """Test analysis endpoint with type error"""
        # Setup mock agent to raise type error
        mock_agent.analyze = AsyncMock(side_effect=TypeError("Type mismatch"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Type mismatch", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_attribute_error(self, mock_agent):
        """Test analysis endpoint with attribute error"""
        # Setup mock agent to raise attribute error
        mock_agent.analyze = AsyncMock(side_effect=AttributeError("Missing attribute"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Missing attribute", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_runtime_error(self, mock_agent):
        """Test analysis endpoint with runtime error"""
        # Setup mock agent to raise runtime error
        mock_agent.analyze = AsyncMock(side_effect=RuntimeError("Runtime error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Runtime error", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_os_error(self, mock_agent):
        """Test analysis endpoint with OS error"""
        # Setup mock agent to raise OS error
        mock_agent.analyze = AsyncMock(side_effect=OSError("OS error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("OS error", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_memory_error(self, mock_agent):
        """Test analysis endpoint with memory error"""
        # Setup mock agent to raise memory error
        mock_agent.analyze = AsyncMock(side_effect=MemoryError("Memory error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Memory error", data["detail"])
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_unicode_error(self, mock_agent):
        """Test analysis endpoint with unicode error"""
        # Setup mock agent to raise unicode error
        mock_agent.analyze = AsyncMock(side_effect=UnicodeError("Unicode error"))
        
        request_data = {
            "query": self.sample_query,
            "context": self.sample_context
        }
        
        response = self.client.post("/analyze", json=request_data)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Unicode error", data["detail"])

class TestBackendApiDataValidation(unittest.TestCase):
    """Test data validation for backend API"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_query_request_validation(self):
        """Test QueryRequest model validation"""
        # Valid request
        valid_request = QueryRequest(
            query="Test query",
            context={"team": "India"}
        )
        self.assertEqual(valid_request.query, "Test query")
        self.assertEqual(valid_request.context, {"team": "India"})
        
        # Test with empty context
        empty_context_request = QueryRequest(query="Test query")
        self.assertEqual(empty_context_request.context, {})
        
        # Test with None context
        none_context_request = QueryRequest(query="Test query", context=None)
        self.assertIsNone(none_context_request.context)
    
    def test_query_response_validation(self):
        """Test QueryResponse model validation"""
        # Valid response
        valid_response = QueryResponse(
            response="Test response",
            analysis={"player": "Virat Kohli"},
            sources=["CricAPI"]
        )
        self.assertEqual(valid_response.response, "Test response")
        self.assertEqual(valid_response.analysis, {"player": "Virat Kohli"})
        self.assertEqual(valid_response.sources, ["CricAPI"])
        
        # Test with empty analysis and sources
        empty_response = QueryResponse(response="Test response")
        self.assertEqual(empty_response.analysis, {})
        self.assertEqual(empty_response.sources, [])
    
    def test_health_response_validation(self):
        """Test HealthResponse model validation"""
        # Valid health response
        valid_health = HealthResponse(
            status="healthy",
            agent_available=True,
            timestamp="2023-01-01T00:00:00"
        )
        self.assertEqual(valid_health.status, "healthy")
        self.assertTrue(valid_health.agent_available)
        self.assertEqual(valid_health.timestamp, "2023-01-01T00:00:00")
        
        # Test with degraded status
        degraded_health = HealthResponse(
            status="degraded",
            agent_available=False,
            timestamp="2023-01-01T00:00:00"
        )
        self.assertEqual(degraded_health.status, "degraded")
        self.assertFalse(degraded_health.agent_available)
    
    def test_query_request_field_validation(self):
        """Test QueryRequest field validation"""
        # Test required field
        with self.assertRaises(ValueError):
            QueryRequest()
        
        # Test min_length validation
        with self.assertRaises(ValueError):
            QueryRequest(query="")
        
        # Test max_length validation
        with self.assertRaises(ValueError):
            QueryRequest(query="A" * 1001)
    
    def test_query_request_context_types(self):
        """Test QueryRequest context with different types"""
        # Test with dict context
        dict_context = QueryRequest(query="Test", context={"key": "value"})
        self.assertIsInstance(dict_context.context, dict)
        
        # Test with list context
        list_context = QueryRequest(query="Test", context=["item1", "item2"])
        self.assertIsInstance(list_context.context, list)
        
        # Test with string context
        string_context = QueryRequest(query="Test", context="string")
        self.assertIsInstance(string_context.context, str)
        
        # Test with int context
        int_context = QueryRequest(query="Test", context=123)
        self.assertIsInstance(int_context.context, int)
        
        # Test with bool context
        bool_context = QueryRequest(query="Test", context=True)
        self.assertIsInstance(bool_context.context, bool)

if __name__ == '__main__':
    unittest.main()
