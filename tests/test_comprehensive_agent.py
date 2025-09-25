"""
Comprehensive Unit Tests for Tactics Master Agent

This module contains comprehensive unit tests for the TacticsMasterAgent class,
including initialization, prompt creation, agent creation, and analysis methods.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from typing import Dict, Any, List

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from agent import TacticsMasterAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor

class TestTacticsMasterAgentComprehensive(unittest.TestCase):
    """Comprehensive test cases for the TacticsMasterAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_llm = Mock(spec=ChatGoogleGenerativeAI)
        self.mock_tools = [Mock(), Mock()]
        self.mock_tools[0].name = "test_tool_1"
        self.mock_tools[1].name = "test_tool_2"
        
    def test_agent_initialization_success(self):
        """Test successful agent initialization"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        self.assertEqual(agent.llm, self.mock_llm)
        self.assertEqual(agent.tools, self.mock_tools)
        self.assertTrue(agent.verbose)
        self.assertIsNone(agent.agent_executor)
    
    def test_agent_initialization_with_verbose_false(self):
        """Test agent initialization with verbose=False"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools, verbose=False)
        
        self.assertEqual(agent.llm, self.mock_llm)
        self.assertEqual(agent.tools, self.mock_tools)
        self.assertFalse(agent.verbose)
        self.assertIsNone(agent.agent_executor)
    
    def test_agent_initialization_with_openai_llm(self):
        """Test agent initialization with OpenAI LLM"""
        mock_openai_llm = Mock(spec=ChatOpenAI)
        agent = TacticsMasterAgent(mock_openai_llm, self.mock_tools)
        
        self.assertEqual(agent.llm, mock_openai_llm)
        self.assertEqual(agent.tools, self.mock_tools)
    
    def test_agent_initialization_llm_none_raises_error(self):
        """Test that agent initialization raises ValueError when llm is None"""
        with self.assertRaises(ValueError) as context:
            TacticsMasterAgent(None, self.mock_tools)
        
        self.assertIn("Language model cannot be None", str(context.exception))
    
    def test_agent_initialization_empty_tools_raises_error(self):
        """Test that agent initialization raises ValueError when tools list is empty"""
        with self.assertRaises(ValueError) as context:
            TacticsMasterAgent(self.mock_llm, [])
        
        self.assertIn("Tools list cannot be empty", str(context.exception))
    
    def test_agent_initialization_none_tools_raises_error(self):
        """Test that agent initialization raises ValueError when tools is None"""
        with self.assertRaises(ValueError) as context:
            TacticsMasterAgent(self.mock_llm, None)
        
        self.assertIn("Tools list cannot be empty", str(context.exception))
    
    def test_create_agent_prompt(self):
        """Test agent prompt creation"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        prompt = agent.create_agent_prompt()
        
        self.assertIsNotNone(prompt)
        # Check that prompt is a ChatPromptTemplate
        self.assertTrue(hasattr(prompt, 'messages'))
    
    def test_get_system_prompt(self):
        """Test system prompt content"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        system_prompt = agent._get_system_prompt()
        
        self.assertIn("Tactics Master", system_prompt)
        self.assertIn("cricket analyst", system_prompt)
        self.assertIn("coaches", system_prompt)
        self.assertIn("tactical decisions", system_prompt)
    
    @patch('app.agent.create_react_agent')
    @patch('app.agent.AgentExecutor')
    def test_create_agent_success(self, mock_agent_executor, mock_create_react_agent):
        """Test successful agent creation"""
        # Setup mocks
        mock_agent = Mock()
        mock_create_react_agent.return_value = mock_agent
        mock_executor = Mock()
        mock_agent_executor.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        result = agent.create_agent()
        
        # Verify agent executor was created
        mock_agent_executor.assert_called_once()
        self.assertEqual(agent.agent_executor, mock_executor)
        self.assertEqual(result, mock_executor)
    
    @patch('app.agent.create_react_agent')
    @patch('app.agent.AgentExecutor')
    def test_create_agent_failure(self, mock_agent_executor, mock_create_react_agent):
        """Test agent creation failure"""
        # Setup mocks to raise exception
        mock_create_react_agent.side_effect = Exception("Agent creation failed")
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        with self.assertRaises(Exception) as context:
            agent.create_agent()
        
        self.assertIn("Failed to create agent", str(context.exception))
    
    def test_analyze_with_empty_query(self):
        """Test analysis with empty query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze("")
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    def test_analyze_with_whitespace_query(self):
        """Test analysis with whitespace-only query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze("   ")
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    def test_analyze_with_none_query(self):
        """Test analysis with None query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze(None)
        
        self.assertFalse(result["success"])
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["intermediate_steps"], [])
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_success(self, mock_agent_executor_class):
        """Test successful analysis"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": [("action", "observation")]
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        agent.agent_executor = mock_executor
        
        result = agent.analyze("Test query")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Test analysis response")
        self.assertEqual(result["intermediate_steps"], [("action", "observation")])
        mock_executor.invoke.assert_called_once()
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_with_context(self, mock_agent_executor_class):
        """Test analysis with context"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": []
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        agent.agent_executor = mock_executor
        
        context = {"team": "India", "opponent": "Australia"}
        result = agent.analyze("Test query", context)
        
        # Verify context was passed to agent
        call_args = mock_executor.invoke.call_args[0][0]
        self.assertEqual(call_args["context"], context)
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_agent_creation_on_demand(self, mock_agent_executor_class):
        """Test that agent executor is created on demand if not initialized"""
        # Setup mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis response",
            "intermediate_steps": []
        }
        mock_agent_executor_class.return_value = mock_executor
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        # Agent executor should be None initially
        self.assertIsNone(agent.agent_executor)
        
        result = agent.analyze("Test query")
        
        # Agent executor should be created
        self.assertIsNotNone(agent.agent_executor)
        self.assertTrue(result["success"])
    
    @patch('app.agent.AgentExecutor')
    def test_analyze_exception_handling(self, mock_agent_executor_class):
        """Test analysis exception handling"""
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
    
    def test_get_available_tools_success(self):
        """Test getting available tools successfully"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        tools = agent.get_available_tools()
        
        self.assertEqual(tools, ["test_tool_1", "test_tool_2"])
    
    def test_get_available_tools_with_exception(self):
        """Test getting available tools with exception"""
        # Create agent with tools that raise exception when accessing name
        mock_tool = Mock()
        mock_tool.name = Mock(side_effect=Exception("Tool name error"))
        agent = TacticsMasterAgent(self.mock_llm, [mock_tool])
        
        tools = agent.get_available_tools()
        
        self.assertEqual(tools, [])
    
    def test_get_agent_info_success(self):
        """Test getting agent info successfully"""
        # Setup LLM with model_name attribute
        self.mock_llm.model_name = "gemini-1.5-flash"
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        info = agent.get_agent_info()
        
        self.assertEqual(info["name"], "Tactics Master")
        self.assertEqual(info["version"], "1.0.0")
        self.assertEqual(info["description"], "AI-powered cricket tactical analysis agent")
        self.assertEqual(info["available_tools"], ["test_tool_1", "test_tool_2"])
        self.assertEqual(info["model"], "gemini-1.5-flash")
        self.assertEqual(info["tools_count"], 2)
        self.assertTrue(info["verbose"])
    
    def test_get_agent_info_with_model_attribute(self):
        """Test getting agent info with model attribute instead of model_name"""
        # Setup LLM with model attribute instead of model_name
        self.mock_llm.model = "gpt-4"
        delattr(self.mock_llm, 'model_name')
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        info = agent.get_agent_info()
        
        self.assertEqual(info["model"], "gpt-4")
    
    def test_get_agent_info_with_no_model_attributes(self):
        """Test getting agent info with no model attributes"""
        # Remove model attributes
        if hasattr(self.mock_llm, 'model_name'):
            delattr(self.mock_llm, 'model_name')
        if hasattr(self.mock_llm, 'model'):
            delattr(self.mock_llm, 'model')
        
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        info = agent.get_agent_info()
        
        self.assertEqual(info["model"], "Unknown")
    
    def test_get_agent_info_with_exception(self):
        """Test getting agent info with exception"""
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

class TestTacticsMasterAgentEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios for TacticsMasterAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_llm = Mock(spec=ChatGoogleGenerativeAI)
        self.mock_tools = [Mock()]
        self.mock_tools[0].name = "test_tool"
    
    def test_analyze_with_very_long_query(self):
        """Test analysis with very long query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        long_query = "Test query " * 1000  # Very long query
        result = agent.analyze(long_query)
        
        # Should handle long queries gracefully
        self.assertIsNotNone(result)
        self.assertIn("response", result)
    
    def test_analyze_with_special_characters(self):
        """Test analysis with special characters in query"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        special_query = "Test query with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = agent.analyze(special_query)
        
        # Should handle special characters gracefully
        self.assertIsNotNone(result)
        self.assertIn("response", result)
    
    def test_analyze_with_unicode_characters(self):
        """Test analysis with unicode characters"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        unicode_query = "Test query with unicode: 你好世界 🌍"
        result = agent.analyze(unicode_query)
        
        # Should handle unicode characters gracefully
        self.assertIsNotNone(result)
        self.assertIn("response", result)
    
    def test_analyze_with_none_context(self):
        """Test analysis with None context"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
        result = agent.analyze("Test query", None)
        
        # Should handle None context gracefully
        self.assertIsNotNone(result)
        self.assertIn("response", result)
    
    def test_analyze_with_complex_context(self):
        """Test analysis with complex context structure"""
        agent = TacticsMasterAgent(self.mock_llm, self.mock_tools)
        
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
        
        result = agent.analyze("Test query", complex_context)
        
        # Should handle complex context gracefully
        self.assertIsNotNone(result)
        self.assertIn("response", result)

if __name__ == '__main__':
    unittest.main()
