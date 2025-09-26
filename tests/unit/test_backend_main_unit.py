"""
Comprehensive Unit Tests for Backend Main Module

This module contains detailed unit tests for the FastAPI backend main module,
covering all endpoints, error handling, and edge cases.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, Any
from fastapi.testclient import TestClient
from fastapi import HTTPException, status

# Mock the hybrid_agent import before importing main
with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
    from backend.main import app, QueryRequest, QueryResponse, HealthResponse


class TestBackendMainModels:
    """Test backend main models and schemas"""
    
    def test_query_request_validation(self):
        """Test QueryRequest model validation"""
        # Valid request
        valid_request = QueryRequest(
            query="Test query",
            context={"team": "India"}
        )
        assert valid_request.query == "Test query"
        assert valid_request.context == {"team": "India"}
        
        # Test with empty context
        empty_context_request = QueryRequest(query="Test query")
        assert empty_context_request.context == {}
        
        # Test with None context
        none_context_request = QueryRequest(query="Test query", context=None)
        assert none_context_request.context is None
    
    def test_query_request_field_validation(self):
        """Test QueryRequest field validation"""
        # Test required field
        with pytest.raises(ValueError):
            QueryRequest()
        
        # Test min_length validation
        with pytest.raises(ValueError):
            QueryRequest(query="")
        
        # Test max_length validation
        with pytest.raises(ValueError):
            QueryRequest(query="A" * 1001)
    
    def test_query_request_context_types(self):
        """Test QueryRequest context with different types"""
        # Test with dict context
        dict_context = QueryRequest(query="Test", context={"key": "value"})
        assert isinstance(dict_context.context, dict)
        
        # Test with list context
        list_context = QueryRequest(query="Test", context=["item1", "item2"])
        assert isinstance(list_context.context, list)
        
        # Test with string context
        string_context = QueryRequest(query="Test", context="string")
        assert isinstance(string_context.context, str)
        
        # Test with int context
        int_context = QueryRequest(query="Test", context=123)
        assert isinstance(int_context.context, int)
        
        # Test with bool context
        bool_context = QueryRequest(query="Test", context=True)
        assert isinstance(bool_context.context, bool)
    
    def test_query_response_validation(self):
        """Test QueryResponse model validation"""
        # Valid response
        valid_response = QueryResponse(
            response="Test response",
            analysis={"player": "Virat Kohli"},
            sources=["CricAPI"]
        )
        assert valid_response.response == "Test response"
        assert valid_response.analysis == {"player": "Virat Kohli"}
        assert valid_response.sources == ["CricAPI"]
        
        # Test with empty analysis and sources
        empty_response = QueryResponse(response="Test response")
        assert empty_response.analysis == {}
        assert empty_response.sources == []
    
    def test_health_response_validation(self):
        """Test HealthResponse model validation"""
        # Valid health response
        valid_health = HealthResponse(
            status="healthy",
            agent_available=True,
            timestamp="2023-01-01T00:00:00"
        )
        assert valid_health.status == "healthy"
        assert valid_health.agent_available is True
        assert valid_health.timestamp == "2023-01-01T00:00:00"
        
        # Test with degraded status
        degraded_health = HealthResponse(
            status="degraded",
            agent_available=False,
            timestamp="2023-01-01T00:00:00"
        )
        assert degraded_health.status == "degraded"
        assert degraded_health.agent_available is False


class TestBackendMainEndpoints:
    """Test backend main endpoints"""
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint"""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["version"] == "1.0.0"
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_success(self, mock_agent, test_client):
        """Test successful analysis endpoint"""
        # Setup mock agent
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test analysis response",
            "analysis": {"player_name": "Virat Kohli"},
            "sources": ["CricAPI"]
        })
        
        request_data = {
            "query": "Analyze Virat Kohli's batting weaknesses",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "analysis" in data
        assert "sources" in data
        assert data["response"] == "Test analysis response"
        assert data["analysis"]["player_name"] == "Virat Kohli"
        assert data["sources"] == ["CricAPI"]
        
        # Verify agent was called with correct parameters
        mock_agent.analyze.assert_called_once_with(
            "Analyze Virat Kohli's batting weaknesses",
            {"team": "India"}
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_without_context(self, mock_agent, test_client):
        """Test analysis endpoint without context"""
        # Setup mock agent
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test analysis response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Analyze Virat Kohli's batting weaknesses"
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "analysis" in data
        assert "sources" in data
        
        # Verify agent was called with empty context
        mock_agent.analyze.assert_called_once_with(
            "Analyze Virat Kohli's batting weaknesses",
            {}
        )
    
    @patch('backend.main.agent', None)
    def test_analyze_endpoint_agent_unavailable(self, test_client):
        """Test analysis endpoint when agent is unavailable"""
        request_data = {
            "query": "Analyze Virat Kohli's batting weaknesses",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 503
        data = response.json()
        assert "detail" in data
        assert "unavailable" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_agent_exception(self, mock_agent, test_client):
        """Test analysis endpoint when agent raises exception"""
        # Setup mock agent to raise exception
        mock_agent.analyze = AsyncMock(side_effect=Exception("Analysis failed"))
        
        request_data = {
            "query": "Analyze Virat Kohli's batting weaknesses",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Analysis failed" in data["detail"]
    
    def test_analyze_endpoint_invalid_request(self, test_client):
        """Test analysis endpoint with invalid request"""
        # Test with missing query
        request_data = {
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_endpoint_empty_query(self, test_client):
        """Test analysis endpoint with empty query"""
        request_data = {
            "query": "",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_endpoint_too_long_query(self, test_client):
        """Test analysis endpoint with query too long"""
        long_query = "A" * 1001  # Exceeds max_length of 1000
        request_data = {
            "query": long_query,
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_endpoint_invalid_json(self, test_client):
        """Test analysis endpoint with invalid JSON"""
        response = test_client.post(
            "/analyze",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_analyze_endpoint_missing_content_type(self, test_client):
        """Test analysis endpoint without content type"""
        response = test_client.post(
            "/analyze",
            data=json.dumps({"query": "Test query"})
        )
        
        # Should still work as FastAPI can handle JSON without explicit content type
        assert response.status_code in [200, 422]
    
    def test_health_endpoint_agent_available(self, test_client):
        """Test health endpoint when agent is available"""
        with patch('backend.main.agent', Mock()):
            response = test_client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "agent_available" in data
            assert "timestamp" in data
            assert data["status"] == "healthy"
            assert data["agent_available"] is True
    
    def test_health_endpoint_agent_unavailable(self, test_client):
        """Test health endpoint when agent is unavailable"""
        with patch('backend.main.agent', None):
            response = test_client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "agent_available" in data
            assert "timestamp" in data
            assert data["status"] == "degraded"
            assert data["agent_available"] is False
    
    def test_health_endpoint_timestamp_format(self, test_client):
        """Test health endpoint timestamp format"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        
        # Should be valid ISO format timestamp
        from datetime import datetime
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")
    
    def test_cors_headers(self, test_client):
        """Test CORS headers are present"""
        response = test_client.options("/analyze")
        
        # Should include CORS headers
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers


class TestBackendMainErrorHandling:
    """Test backend main error handling scenarios"""
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_network_timeout(self, mock_agent, test_client):
        """Test analysis endpoint with network timeout"""
        # Setup mock agent to raise timeout exception
        mock_agent.analyze = AsyncMock(side_effect=TimeoutError("Request timeout"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "timeout" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_connection_error(self, mock_agent, test_client):
        """Test analysis endpoint with connection error"""
        # Setup mock agent to raise connection error
        mock_agent.analyze = AsyncMock(side_effect=ConnectionError("Connection failed"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Connection failed" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_value_error(self, mock_agent, test_client):
        """Test analysis endpoint with value error"""
        # Setup mock agent to raise value error
        mock_agent.analyze = AsyncMock(side_effect=ValueError("Invalid value"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Invalid value" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_key_error(self, mock_agent, test_client):
        """Test analysis endpoint with key error"""
        # Setup mock agent to raise key error
        mock_agent.analyze = AsyncMock(side_effect=KeyError("Missing key"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Missing key" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_type_error(self, mock_agent, test_client):
        """Test analysis endpoint with type error"""
        # Setup mock agent to raise type error
        mock_agent.analyze = AsyncMock(side_effect=TypeError("Type mismatch"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Type mismatch" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_attribute_error(self, mock_agent, test_client):
        """Test analysis endpoint with attribute error"""
        # Setup mock agent to raise attribute error
        mock_agent.analyze = AsyncMock(side_effect=AttributeError("Missing attribute"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Missing attribute" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_runtime_error(self, mock_agent, test_client):
        """Test analysis endpoint with runtime error"""
        # Setup mock agent to raise runtime error
        mock_agent.analyze = AsyncMock(side_effect=RuntimeError("Runtime error"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Runtime error" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_os_error(self, mock_agent, test_client):
        """Test analysis endpoint with OS error"""
        # Setup mock agent to raise OS error
        mock_agent.analyze = AsyncMock(side_effect=OSError("OS error"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "OS error" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_memory_error(self, mock_agent, test_client):
        """Test analysis endpoint with memory error"""
        # Setup mock agent to raise memory error
        mock_agent.analyze = AsyncMock(side_effect=MemoryError("Memory error"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Memory error" in data["detail"]
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_unicode_error(self, mock_agent, test_client):
        """Test analysis endpoint with unicode error"""
        # Setup mock agent to raise unicode error
        mock_agent.analyze = AsyncMock(side_effect=UnicodeError("Unicode error"))
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Unicode error" in data["detail"]


class TestBackendMainEdgeCases:
    """Test backend main edge cases"""
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_complex_context(self, mock_agent, test_client):
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
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Test query",
            "context": complex_context
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
        # Verify agent was called with complex context
        mock_agent.analyze.assert_called_once_with(
            "Test query",
            complex_context
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_unicode_query(self, mock_agent, test_client):
        """Test analysis endpoint with unicode query"""
        unicode_query = "Analyze Virat Kohli's batting weaknesses 分析"
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Unicode analysis response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": unicode_query,
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
        # Verify agent was called with unicode query
        mock_agent.analyze.assert_called_once_with(
            unicode_query,
            {"team": "India"}
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_special_characters(self, mock_agent, test_client):
        """Test analysis endpoint with special characters"""
        special_query = "Analyze Virat Kohli's batting!@#$%^&*()"
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Special characters analysis response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": special_query,
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
        # Verify agent was called with special characters
        mock_agent.analyze.assert_called_once_with(
            special_query,
            {"team": "India"}
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_none_context(self, mock_agent, test_client):
        """Test analysis endpoint with None context"""
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Test query",
            "context": None
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
        # Verify agent was called with None context
        mock_agent.analyze.assert_called_once_with(
            "Test query",
            None
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_empty_context(self, mock_agent, test_client):
        """Test analysis endpoint with empty context"""
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Test query",
            "context": {}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        
        # Verify agent was called with empty context
        mock_agent.analyze.assert_called_once_with(
            "Test query",
            {}
        )
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_with_large_context(self, mock_agent, test_client):
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
        
        # Verify agent was called with large context
        mock_agent.analyze.assert_called_once_with(
            "Test query",
            large_context
        )


class TestBackendMainPerformance:
    """Test backend main performance scenarios"""
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_performance(self, mock_agent, test_client):
        """Test analysis endpoint performance"""
        import time
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        start_time = time.time()
        
        for _ in range(10):
            response = test_client.post("/analyze", json=request_data)
            assert response.status_code == 200
        
        end_time = time.time()
        
        # Should complete 10 requests in less than 5 seconds
        assert (end_time - start_time) < 5.0
    
    def test_health_endpoint_performance(self, test_client):
        """Test health endpoint performance"""
        import time
        
        start_time = time.time()
        
        for _ in range(100):
            response = test_client.get("/health")
            assert response.status_code == 200
        
        end_time = time.time()
        
        # Should complete 100 requests in less than 2 seconds
        assert (end_time - start_time) < 2.0
    
    def test_root_endpoint_performance(self, test_client):
        """Test root endpoint performance"""
        import time
        
        start_time = time.time()
        
        for _ in range(100):
            response = test_client.get("/")
            assert response.status_code == 200
        
        end_time = time.time()
        
        # Should complete 100 requests in less than 1 second
        assert (end_time - start_time) < 1.0


class TestBackendMainMemoryUsage:
    """Test backend main memory usage scenarios"""
    
    @patch('backend.main.agent')
    def test_analyze_endpoint_memory_usage(self, mock_agent, test_client):
        """Test analysis endpoint memory usage"""
        import sys
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        request_data = {
            "query": "Test query",
            "context": {"team": "India"}
        }
        
        response = test_client.post("/analyze", json=request_data)
        
        # Response should not be excessively large
        assert sys.getsizeof(response.content) < 50000  # Less than 50KB
    
    def test_health_endpoint_memory_usage(self, test_client):
        """Test health endpoint memory usage"""
        import sys
        
        response = test_client.get("/health")
        
        # Response should not be excessively large
        assert sys.getsizeof(response.content) < 1000  # Less than 1KB
    
    def test_root_endpoint_memory_usage(self, test_client):
        """Test root endpoint memory usage"""
        import sys
        
        response = test_client.get("/")
        
        # Response should not be excessively large
        assert sys.getsizeof(response.content) < 1000  # Less than 1KB


class TestBackendMainConcurrency:
    """Test backend main concurrency scenarios"""
    
    @patch('backend.main.agent')
    def test_concurrent_requests(self, mock_agent, test_client):
        """Test concurrent requests handling"""
        import threading
        import time
        
        mock_agent.analyze = AsyncMock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        results = []
        
        def make_request():
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
    
    def test_concurrent_health_requests(self, test_client):
        """Test concurrent health requests"""
        import threading
        import time
        
        results = []
        
        def make_health_request():
            response = test_client.get("/health")
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_health_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == 10
        for status_code in results:
            assert status_code == 200
