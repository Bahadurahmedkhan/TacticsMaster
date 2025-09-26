"""
Comprehensive Unit Tests for TacticsMasterAgent

This module contains detailed unit tests for the TacticsMasterAgent class,
covering all methods, edge cases, and error scenarios.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

from app.agent import TacticsMasterAgent
from app.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ValidationError
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor


class TestTacticsMasterAgentInitialization:
    """Test agent initialization scenarios"""
    
    def test_agent_initialization_success(self, mock_llm, mock_tools):
        """Test successful agent initialization"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        assert agent.llm == mock_llm
        assert agent.tools == mock_tools
        assert agent.verbose is True
        assert agent.agent_executor is None
    
    def test_agent_initialization_with_verbose_false(self, mock_llm, mock_tools):
        """Test agent initialization with verbose=False"""
        agent = TacticsMasterAgent(mock_llm, mock_tools, verbose=False)
        
        assert agent.llm == mock_llm
        assert agent.tools == mock_tools
        assert agent.verbose is False
        assert agent.agent_executor is None
    
    def test_agent_initialization_with_openai_llm(self, mock_tools):
        """Test agent initialization with OpenAI LLM"""
        mock_openai_llm = Mock(spec=ChatOpenAI)
        agent = TacticsMasterAgent(mock_openai_llm, mock_tools)
        
        assert agent.llm == mock_openai_llm
        assert agent.tools == mock_tools
    
    def test_agent_initialization_with_gemini_llm(self, mock_tools):
        """Test agent initialization with Gemini LLM"""
        mock_gemini_llm = Mock(spec=ChatGoogleGenerativeAI)
        agent = TacticsMasterAgent(mock_gemini_llm, mock_tools)
        
        assert agent.llm == mock_gemini_llm
        assert agent.tools == mock_tools
    
    def test_agent_initialization_llm_none_raises_error(self, mock_tools):
        """Test that agent initialization raises error when llm is None"""
        with pytest.raises(AgentInitializationError) as exc_info:
            TacticsMasterAgent(None, mock_tools)
        
        assert "Language model cannot be None" in str(exc_info.value)
        assert exc_info.value.error_code == "INVALID_LLM"
    
    def test_agent_initialization_empty_tools_raises_error(self, mock_llm):
        """Test that agent initialization raises error when tools list is empty"""
        with pytest.raises(AgentInitializationError) as exc_info:
            TacticsMasterAgent(mock_llm, [])
        
        assert "Tools list cannot be empty" in str(exc_info.value)
        assert exc_info.value.error_code == "EMPTY_TOOLS_LIST"
    
    def test_agent_initialization_none_tools_raises_error(self, mock_llm):
        """Test that agent initialization raises error when tools is None"""
        with pytest.raises(AgentInitializationError) as exc_info:
            TacticsMasterAgent(mock_llm, None)
        
        assert "Tools list cannot be empty" in str(exc_info.value)
        assert exc_info.value.error_code == "EMPTY_TOOLS_LIST"


class TestTacticsMasterAgentPromptCreation:
    """Test agent prompt creation functionality"""
    
    def test_create_agent_prompt(self, mock_llm, mock_tools):
        """Test agent prompt creation"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        prompt = agent.create_agent_prompt()
        
        assert prompt is not None
        assert hasattr(prompt, 'messages')
        assert len(prompt.messages) == 3  # system, human, placeholder
    
    def test_get_system_prompt_content(self, mock_llm, mock_tools):
        """Test system prompt content"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        system_prompt = agent._get_system_prompt()
        
        assert "Tactics Master" in system_prompt
        assert "cricket analyst" in system_prompt
        assert "coaches" in system_prompt
        assert "tactical decisions" in system_prompt
        assert "get_player_stats" in system_prompt
        assert "analyze_weaknesses" in system_prompt
        assert "generate_bowling_plan" in system_prompt


class TestTacticsMasterAgentCreation:
    """Test agent creation functionality"""
    
    @patch('app.agent.create_react_agent')
    @patch('app.agent.AgentExecutor')
    def test_create_agent_success(self, mock_agent_executor_class, mock_create_react_agent, mock_llm, mock_tools):
        """Test successful agent creation"""
        # Setup mocks
        mock_agent = Mock()
        mock_create_react_agent.return_value = mock_agent
        mock_executor = Mock()
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        result = agent.create_agent()
        
        # Verify agent executor was created
        mock_agent_executor_class.assert_called_once()
        assert agent.agent_executor == mock_executor
        assert result == mock_executor
    
    @patch('app.agent.create_react_agent')
    def test_create_agent_failure(self, mock_create_react_agent, mock_llm, mock_tools):
        """Test agent creation failure"""
        # Setup mocks to raise exception
        mock_create_react_agent.side_effect = Exception("Agent creation failed")
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        with pytest.raises(AgentInitializationError) as exc_info:
            agent.create_agent()
        
        assert "Failed to create agent" in str(exc_info.value)
        assert exc_info.value.error_code == "AGENT_CREATION_FAILED"


class TestTacticsMasterAgentAnalysis:
    """Test agent analysis functionality"""
    
    def test_analyze_with_empty_query(self, mock_llm, mock_tools):
        """Test analysis with empty query"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        with pytest.raises(ValidationError) as exc_info:
            agent.analyze("")
        
        assert "Query cannot be empty" in str(exc_info.value)
        assert exc_info.value.error_code == "EMPTY_QUERY"
    
    def test_analyze_with_whitespace_query(self, mock_llm, mock_tools):
        """Test analysis with whitespace-only query"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        with pytest.raises(ValidationError) as exc_info:
            agent.analyze("   ")
        
        assert "Query cannot be empty" in str(exc_info.value)
        assert exc_info.value.error_code == "EMPTY_QUERY"
    
    def test_analyze_with_none_query(self, mock_llm, mock_tools):
        """Test analysis with None query"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        with pytest.raises(ValidationError) as exc_info:
            agent.analyze(None)
        
        assert "Query cannot be empty" in str(exc_info.value)
        assert exc_info.value.error_code == "EMPTY_QUERY"
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_success(self, mock_agent_executor_class, mock_llm, mock_tools):
        """Test successful analysis"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": [("action", "observation")]
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        agent.agent_executor = mock_executor
        
        result = agent.analyze("Test query")
        
        assert result["success"] is True
        assert result["response"] == "Test analysis response"
        assert result["intermediate_steps"] == [("action", "observation")]
        mock_executor.invoke.assert_called_once()
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_with_context(self, mock_agent_executor_class, mock_llm, mock_tools):
        """Test analysis with context"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": []
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        agent.agent_executor = mock_executor
        
        context = {"team": "India", "opponent": "Australia"}
        result = agent.analyze("Test query", context)
        
        # Verify context was passed to agent
        call_args = mock_executor.invoke.call_args[0][0]
        assert call_args["context"] == context
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_agent_creation_on_demand(self, mock_agent_executor_class, mock_llm, mock_tools):
        """Test that agent executor is created on demand if not initialized"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": []
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Agent executor should be None initially
        assert agent.agent_executor is None
        
        result = agent.analyze("Test query")
        
        # Agent executor should be created
        assert agent.agent_executor is not None
        assert result["success"] is True
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_exception_handling(self, mock_agent_executor_class, mock_llm, mock_tools):
        """Test analysis exception handling"""
        # Setup mock agent executor to raise exception
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("Analysis failed")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        agent.agent_executor = mock_executor
        
        with pytest.raises(AgentExecutionError) as exc_info:
            agent.analyze("Test query")
        
        assert "Analysis failed" in str(exc_info.value)
        assert exc_info.value.error_code == "ANALYSIS_EXECUTION_ERROR"


class TestTacticsMasterAgentUtilityMethods:
    """Test agent utility methods"""
    
    def test_get_available_tools_success(self, mock_llm, mock_tools):
        """Test getting available tools successfully"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        tools = agent.get_available_tools()
        
        expected_tools = [tool.name for tool in mock_tools]
        assert tools == expected_tools
    
    def test_get_available_tools_with_exception(self, mock_llm):
        """Test getting available tools with exception"""
        # Create agent with tools that raise exception when accessing name
        mock_tool = Mock()
        mock_tool.name = Mock(side_effect=Exception("Tool name error"))
        agent = TacticsMasterAgent(mock_llm, [mock_tool])
        
        tools = agent.get_available_tools()
        
        assert tools == []
    
    def test_get_agent_info_success(self, mock_llm, mock_tools):
        """Test getting agent info successfully"""
        # Setup LLM with model_name attribute
        mock_llm.model_name = "gemini-1.5-flash"
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        info = agent.get_agent_info()
        
        assert info["name"] == "Tactics Master"
        assert info["version"] == "1.0.0"
        assert info["description"] == "AI-powered cricket tactical analysis agent"
        assert info["available_tools"] == [tool.name for tool in mock_tools]
        assert info["model"] == "gemini-1.5-flash"
        assert info["tools_count"] == len(mock_tools)
        assert info["verbose"] is True
    
    def test_get_agent_info_with_model_attribute(self, mock_llm, mock_tools):
        """Test getting agent info with model attribute instead of model_name"""
        # Setup LLM with model attribute instead of model_name
        mock_llm.model = "gpt-4"
        delattr(mock_llm, 'model_name')
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        info = agent.get_agent_info()
        
        assert info["model"] == "gpt-4"
    
    def test_get_agent_info_with_no_model_attributes(self, mock_llm, mock_tools):
        """Test getting agent info with no model attributes"""
        # Remove model attributes
        if hasattr(mock_llm, 'model_name'):
            delattr(mock_llm, 'model_name')
        if hasattr(mock_llm, 'model'):
            delattr(mock_llm, 'model')
        
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        info = agent.get_agent_info()
        
        assert info["model"] == "Unknown"
    
    def test_get_agent_info_with_exception(self, mock_llm):
        """Test getting agent info with exception"""
        # Create agent with tools that raise exception
        mock_tool = Mock()
        mock_tool.name = Mock(side_effect=Exception("Tool error"))
        agent = TacticsMasterAgent(mock_llm, [mock_tool])
        
        info = agent.get_agent_info()
        
        assert info["name"] == "Tactics Master"
        assert info["version"] == "1.0.0"
        assert info["available_tools"] == []
        assert info["tools_count"] == 0
        assert info["verbose"] is False


class TestTacticsMasterAgentEdgeCases:
    """Test edge cases and error scenarios"""
    
    def test_analyze_with_very_long_query(self, mock_llm, mock_tools):
        """Test analysis with very long query"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        long_query = "Test query " * 1000  # Very long query
        
        # Should not raise exception for long queries
        with patch('app.agent.AgentExecutor') as mock_agent_executor_class:
            mock_executor = Mock()
            mock_executor.invoke.return_value = {
                "output": "Test response",
                "intermediate_steps": []
            }
            mock_agent_executor_class.return_value = mock_executor
            
            agent.agent_executor = mock_executor
            result = agent.analyze(long_query)
            
            assert result["success"] is True
    
    def test_analyze_with_special_characters(self, mock_llm, mock_tools):
        """Test analysis with special characters in query"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        special_query = "Test query with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        with patch('app.agent.AgentExecutor') as mock_agent_executor_class:
            mock_executor = Mock()
            mock_executor.invoke.return_value = {
                "output": "Test response",
                "intermediate_steps": []
            }
            mock_agent_executor_class.return_value = mock_executor
            
            agent.agent_executor = mock_executor
            result = agent.analyze(special_query)
            
            assert result["success"] is True
    
    def test_analyze_with_unicode_characters(self, mock_llm, mock_tools):
        """Test analysis with unicode characters"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        unicode_query = "Test query with unicode: 你好世界 🌍"
        
        with patch('app.agent.AgentExecutor') as mock_agent_executor_class:
            mock_executor = Mock()
            mock_executor.invoke.return_value = {
                "output": "Test response",
                "intermediate_steps": []
            }
            mock_agent_executor_class.return_value = mock_executor
            
            agent.agent_executor = mock_executor
            result = agent.analyze(unicode_query)
            
            assert result["success"] is True
    
    def test_analyze_with_none_context(self, mock_llm, mock_tools):
        """Test analysis with None context"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        with patch('app.agent.AgentExecutor') as mock_agent_executor_class:
            mock_executor = Mock()
            mock_executor.invoke.return_value = {
                "output": "Test response",
                "intermediate_steps": []
            }
            mock_agent_executor_class.return_value = mock_executor
            
            agent.agent_executor = mock_executor
            result = agent.analyze("Test query", None)
            
            assert result["success"] is True
    
    def test_analyze_with_complex_context(self, mock_llm, mock_tools):
        """Test analysis with complex context structure"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        complex_context = {
            "team": "India",
            "players": ["Virat Kohli", "Rohit Sharma"],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {"pitch": "batting_friendly", "weather": "clear"}
            },
            "nested": {
                "deep": {
                    "value": "test"
                }
            }
        }
        
        with patch('app.agent.AgentExecutor') as mock_agent_executor_class:
            mock_executor = Mock()
            mock_executor.invoke.return_value = {
                "output": "Test response",
                "intermediate_steps": []
            }
            mock_agent_executor_class.return_value = mock_executor
            
            agent.agent_executor = mock_executor
            result = agent.analyze("Test query", complex_context)
            
            assert result["success"] is True


class TestTacticsMasterAgentPerformance:
    """Test agent performance scenarios"""
    
    def test_agent_initialization_performance(self, mock_llm, mock_tools):
        """Test agent initialization performance"""
        import time
        
        start_time = time.time()
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        end_time = time.time()
        
        # Should initialize quickly (less than 1 second)
        assert (end_time - start_time) < 1.0
    
    def test_agent_info_retrieval_performance(self, mock_llm, mock_tools):
        """Test agent info retrieval performance"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        import time
        start_time = time.time()
        
        for _ in range(100):
            info = agent.get_agent_info()
            assert info["name"] == "Tactics Master"
        
        end_time = time.time()
        
        # Should be fast (less than 1 second for 100 calls)
        assert (end_time - start_time) < 1.0
    
    def test_tools_retrieval_performance(self, mock_llm, mock_tools):
        """Test tools retrieval performance"""
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        import time
        start_time = time.time()
        
        for _ in range(100):
            tools = agent.get_available_tools()
            assert len(tools) == len(mock_tools)
        
        end_time = time.time()
        
        # Should be fast (less than 1 second for 100 calls)
        assert (end_time - start_time) < 1.0


class TestTacticsMasterAgentMemoryUsage:
    """Test agent memory usage scenarios"""
    
    def test_agent_memory_usage(self, mock_llm, mock_tools):
        """Test agent memory usage"""
        import sys
        
        # Get initial memory usage
        initial_size = sys.getsizeof(mock_llm) + sys.getsizeof(mock_tools)
        
        # Create agent
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Get agent memory usage
        agent_size = sys.getsizeof(agent)
        
        # Agent should not use excessive memory
        assert agent_size < 10000  # Less than 10KB
    
    def test_agent_with_large_tools_list(self, mock_llm):
        """Test agent with large tools list"""
        # Create large tools list
        large_tools = [Mock() for _ in range(1000)]
        for i, tool in enumerate(large_tools):
            tool.name = f"tool_{i}"
        
        agent = TacticsMasterAgent(mock_llm, large_tools)
        
        # Should handle large tools list
        assert len(agent.tools) == 1000
        assert len(agent.get_available_tools()) == 1000
