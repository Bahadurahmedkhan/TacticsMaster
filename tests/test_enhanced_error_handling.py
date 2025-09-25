"""
Enhanced Error Handling Tests for Tactics Master System

This module tests the enhanced error handling with specific exception types
and improved error reporting throughout the application.

Author: Tactics Master Team
Version: 1.0.0
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from typing import Dict, Any

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import custom exceptions
from exceptions import (
    TacticsMasterError,
    AgentInitializationError,
    AgentExecutionError,
    ToolExecutionError,
    CricketDataError,
    APIConnectionError,
    APITimeoutError,
    APIResponseError,
    DataValidationError,
    ConfigurationError,
    AnalysisError,
    NetworkError,
    AuthenticationError,
    RateLimitError,
    DataProcessingError,
    ValidationError,
    ServiceUnavailableError
)

# Import components to test
from agent import TacticsMasterAgent
from tools.cricket_api_tools import get_player_stats, get_team_squad
from tools.tactical_tools import analyze_weaknesses, find_best_matchup

class TestCustomExceptions(unittest.TestCase):
    """Test custom exception classes"""
    
    def test_tactics_master_error_base(self):
        """Test base TacticsMasterError exception"""
        error = TacticsMasterError("Test error", "TEST_CODE", {"key": "value"})
        
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.error_code, "TEST_CODE")
        self.assertEqual(error.context, {"key": "value"})
        self.assertIsInstance(error, Exception)
    
    def test_agent_initialization_error(self):
        """Test AgentInitializationError"""
        error = AgentInitializationError("Agent init failed", "INIT_ERROR", {"llm": "test"})
        
        self.assertEqual(error.message, "Agent init failed")
        self.assertEqual(error.error_code, "INIT_ERROR")
        self.assertEqual(error.context, {"llm": "test"})
        self.assertIsInstance(error, TacticsMasterError)
    
    def test_agent_execution_error(self):
        """Test AgentExecutionError"""
        error = AgentExecutionError("Agent execution failed", "EXEC_ERROR", {"query": "test"})
        
        self.assertEqual(error.message, "Agent execution failed")
        self.assertEqual(error.error_code, "EXEC_ERROR")
        self.assertEqual(error.context, {"query": "test"})
        self.assertIsInstance(error, TacticsMasterError)
    
    def test_cricket_data_error(self):
        """Test CricketDataError"""
        error = CricketDataError("Cricket data failed", "DATA_ERROR", {"player": "test"})
        
        self.assertEqual(error.message, "Cricket data failed")
        self.assertEqual(error.error_code, "DATA_ERROR")
        self.assertEqual(error.context, {"player": "test"})
        self.assertIsInstance(error, TacticsMasterError)
    
    def test_api_connection_error(self):
        """Test APIConnectionError"""
        error = APIConnectionError("API connection failed", "CONN_ERROR", {"url": "test"})
        
        self.assertEqual(error.message, "API connection failed")
        self.assertEqual(error.error_code, "CONN_ERROR")
        self.assertEqual(error.context, {"url": "test"})
        self.assertIsInstance(error, TacticsMasterError)
    
    def test_validation_error(self):
        """Test ValidationError"""
        error = ValidationError("Validation failed", "VALID_ERROR", {"field": "test"})
        
        self.assertEqual(error.message, "Validation failed")
        self.assertEqual(error.error_code, "VALID_ERROR")
        self.assertEqual(error.context, {"field": "test"})
        self.assertIsInstance(error, TacticsMasterError)

class TestAgentEnhancedErrorHandling(unittest.TestCase):
    """Test enhanced error handling in TacticsMasterAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_llm = Mock()
        self.mock_tools = [Mock(), Mock()]
        self.mock_tools[0].name = "test_tool_1"
        self.mock_tools[1].name = "test_tool_2"
    
    def test_agent_initialization_with_none_llm(self):
        """Test agent initialization with None LLM raises AgentInitializationError"""
        with self.assertRaises(AgentInitializationError) as context:
            TacticsMasterAgent(None, self.mock_tools)
        
        error = context.exception
        self.assertEqual(error.error_code, "INVALID_LLM")
        self.assertIn("Language model cannot be None", error.message)
    
    def test_agent_initialization_with_empty_tools(self):
        """Test agent initialization with empty tools raises AgentInitializationError"""
        with self.assertRaises(AgentInitializationError) as context:
            TacticsMasterAgent(self.mock_llm, [])
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_TOOLS_LIST")
        self.assertIn("Tools list cannot be empty", error.message)
    
    def test_agent_analyze_empty_query_raises_validation_error(self):
        """Test agent analyze with empty query raises ValidationError"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        with self.assertRaises(ValidationError) as context:
            agent.analyze("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_QUERY")
        self.assertIn("Query cannot be empty", error.message)
    
    def test_agent_analyze_whitespace_query_raises_validation_error(self):
        """Test agent analyze with whitespace-only query raises ValidationError"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        with self.assertRaises(ValidationError) as context:
            agent.analyze("   ")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_QUERY")
        self.assertIn("Query cannot be empty", error.message)
    
    @patch('app.agent.AgentExecutor')
    def test_agent_analyze_execution_error(self, mock_agent_executor_class):
        """Test agent analyze raises AgentExecutionError on failure"""
        # Setup mock agent executor to raise exception
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("Analysis failed")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        agent.agent_executor = mock_executor
        
        with self.assertRaises(AgentExecutionError) as context:
            agent.analyze("Test query")
        
        error = context.exception
        self.assertEqual(error.error_code, "ANALYSIS_EXECUTION_ERROR")
        self.assertIn("Analysis failed", error.message)

class TestCricketApiToolsEnhancedErrorHandling(unittest.TestCase):
    """Test enhanced error handling in cricket API tools"""
    
    def test_get_player_stats_empty_name_raises_validation_error(self):
        """Test get_player_stats with empty name raises DataValidationError"""
        with self.assertRaises(DataValidationError) as context:
            get_player_stats("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_NAME")
        self.assertIn("Player name cannot be empty", error.message)
    
    def test_get_player_stats_whitespace_name_raises_validation_error(self):
        """Test get_player_stats with whitespace name raises DataValidationError"""
        with self.assertRaises(DataValidationError) as context:
            get_player_stats("   ")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_NAME")
        self.assertIn("Player name cannot be empty", error.message)
    
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_get_player_stats_connection_error(self, mock_get):
        """Test get_player_stats raises APIConnectionError on connection failure"""
        mock_get.side_effect = ConnectionError("Connection failed")
        
        with self.assertRaises(APIConnectionError) as context:
            get_player_stats("Test Player")
        
        error = context.exception
        self.assertEqual(error.error_code, "API_CONNECTION_ERROR")
        self.assertIn("Failed to connect to cricket data API", error.message)
        self.assertEqual(error.context["player_name"], "Test Player")
    
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_get_player_stats_timeout_error(self, mock_get):
        """Test get_player_stats raises APITimeoutError on timeout"""
        mock_get.side_effect = TimeoutError("Request timeout")
        
        with self.assertRaises(APITimeoutError) as context:
            get_player_stats("Test Player")
        
        error = context.exception
        self.assertEqual(error.error_code, "API_TIMEOUT_ERROR")
        self.assertIn("Cricket data API request timed out", error.message)
        self.assertEqual(error.context["player_name"], "Test Player")
    
    @patch('app.tools.cricket_api_tools.requests.get')
    def test_get_player_stats_http_error(self, mock_get):
        """Test get_player_stats raises APIResponseError on HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.side_effect = HTTPError("HTTP error", response=mock_response)
        
        with self.assertRaises(APIResponseError) as context:
            get_player_stats("Test Player")
        
        error = context.exception
        self.assertEqual(error.error_code, "API_HTTP_ERROR")
        self.assertIn("Cricket data API returned error", error.message)
        self.assertEqual(error.context["status_code"], 500)

class TestTacticalToolsEnhancedErrorHandling(unittest.TestCase):
    """Test enhanced error handling in tactical tools"""
    
    def test_analyze_weaknesses_empty_data_raises_validation_error(self):
        """Test analyze_weaknesses with empty data raises DataValidationError"""
        with self.assertRaises(DataValidationError) as context:
            analyze_weaknesses("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_DATA")
        self.assertIn("Player data cannot be empty", error.message)
    
    def test_analyze_weaknesses_whitespace_data_raises_validation_error(self):
        """Test analyze_weaknesses with whitespace data raises DataValidationError"""
        with self.assertRaises(DataValidationError) as context:
            analyze_weaknesses("   ")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_DATA")
        self.assertIn("Player data cannot be empty", error.message)
    
    def test_analyze_weaknesses_invalid_json_raises_validation_error(self):
        """Test analyze_weaknesses with invalid JSON raises DataValidationError"""
        with self.assertRaises(DataValidationError) as context:
            analyze_weaknesses("invalid json")
        
        error = context.exception
        self.assertEqual(error.error_code, "INVALID_JSON_DATA")
        self.assertIn("Invalid player data format", error.message)
    
    def test_analyze_weaknesses_analysis_error(self):
        """Test analyze_weaknesses raises AnalysisError on processing failure"""
        # Create valid JSON but with data that causes processing error
        valid_json = json.dumps({"player_name": "Test Player"})
        
        with patch('app.tools.tactical_tools._assess_player_overall') as mock_assess:
            mock_assess.side_effect = Exception("Processing failed")
            
            with self.assertRaises(AnalysisError) as context:
                analyze_weaknesses(valid_json)
            
            error = context.exception
            self.assertEqual(error.error_code, "WEAKNESS_ANALYSIS_ERROR")
            self.assertIn("Weakness analysis failed", error.message)

class TestErrorHandlingIntegration(unittest.TestCase):
    """Test error handling integration across components"""
    
    def test_error_propagation_chain(self):
        """Test that errors propagate correctly through the system"""
        # Test that ValidationError from tools propagates to agent
        mock_llm = Mock()
        mock_tools = [Mock()]
        mock_tools[0].name = "test_tool"
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Mock tool to raise ValidationError
        with patch('app.tools.cricket_api_tools.get_player_stats') as mock_tool:
            mock_tool.side_effect = DataValidationError("Tool validation failed", "TOOL_ERROR")
            
            with self.assertRaises(AgentExecutionError):
                agent.analyze("Test query")
    
    def test_error_context_preservation(self):
        """Test that error context is preserved through the system"""
        try:
            raise DataValidationError(
                message="Test validation error",
                error_code="TEST_ERROR",
                context={"field": "test_field", "value": "test_value"}
            )
        except DataValidationError as e:
            self.assertEqual(e.message, "Test validation error")
            self.assertEqual(e.error_code, "TEST_ERROR")
            self.assertEqual(e.context["field"], "test_field")
            self.assertEqual(e.context["value"], "test_value")
    
    def test_error_hierarchy(self):
        """Test that error hierarchy is maintained"""
        # Test that specific errors inherit from base
        self.assertIsInstance(AgentInitializationError(), TacticsMasterError)
        self.assertIsInstance(AgentExecutionError(), TacticsMasterError)
        self.assertIsInstance(CricketDataError(), TacticsMasterError)
        self.assertIsInstance(ValidationError(), TacticsMasterError)
        
        # Test that specific errors are not instances of other specific errors
        self.assertNotIsInstance(AgentInitializationError(), AgentExecutionError)
        self.assertNotIsInstance(CricketDataError(), ValidationError)

class TestErrorHandlingEdgeCases(unittest.TestCase):
    """Test edge cases in error handling"""
    
    def test_error_with_none_context(self):
        """Test error creation with None context"""
        error = TacticsMasterError("Test error", "TEST_CODE", None)
        self.assertEqual(error.context, {})
    
    def test_error_with_empty_context(self):
        """Test error creation with empty context"""
        error = TacticsMasterError("Test error", "TEST_CODE", {})
        self.assertEqual(error.context, {})
    
    def test_error_message_formatting(self):
        """Test error message formatting"""
        error = TacticsMasterError("Test error with {placeholder}", "TEST_CODE", {"placeholder": "value"})
        self.assertEqual(error.message, "Test error with {placeholder}")
    
    def test_error_code_validation(self):
        """Test error code validation"""
        error = TacticsMasterError("Test error", "VALID_CODE_123", {})
        self.assertEqual(error.error_code, "VALID_CODE_123")
    
    def test_error_context_types(self):
        """Test error context with different types"""
        context = {
            "string": "test",
            "integer": 123,
            "float": 45.67,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "none": None
        }
        
        error = TacticsMasterError("Test error", "TEST_CODE", context)
        self.assertEqual(error.context, context)

if __name__ == '__main__':
    unittest.main()
