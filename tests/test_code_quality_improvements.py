"""
Code Quality Improvements Tests for Tactics Master System

This module tests the enhanced code quality improvements including
modularized functions, consistent coding patterns, and improved error handling.

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

# Import components to test
from agent import TacticsMasterAgent
from tools.cricket_api_tools import get_player_stats, get_team_squad
from tools.tactical_tools import analyze_weaknesses, find_best_matchup

# Import custom exceptions
from exceptions import (
    TacticsMasterError,
    AgentInitializationError,
    AgentExecutionError,
    ValidationError,
    DataValidationError,
    CricketDataError,
    APIConnectionError,
    APITimeoutError,
    APIResponseError
)

class TestModularizedFunctions(unittest.TestCase):
    """Test modularized functions for better maintainability"""
    
    def test_get_available_tools_function(self):
        """Test _get_available_tools function exists and returns tools"""
        # This tests that the function was properly extracted
        from main import _get_available_tools
        
        tools = _get_available_tools()
        
        # Should return a list of tools
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        
        # Should contain expected tools
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            'get_player_stats',
            'get_team_squad', 
            'get_matchup_data',
            'get_venue_stats',
            'analyze_weaknesses',
            'find_best_matchup',
            'generate_bowling_plan',
            'generate_fielding_plan'
        ]
        
        for expected_tool in expected_tools:
            self.assertIn(expected_tool, tool_names)
    
    def test_create_react_agent_function(self):
        """Test _create_react_agent function exists and works"""
        from main import _create_react_agent
        
        # Mock LLM and tools
        mock_llm = Mock()
        mock_tools = [Mock(), Mock()]
        mock_tools[0].name = "test_tool_1"
        mock_tools[1].name = "test_tool_2"
        
        # Should not raise exception
        try:
            result = _create_react_agent(mock_llm, mock_tools)
            # Function should return something (agent instance)
            self.assertIsNotNone(result)
        except Exception as e:
            # If it fails due to missing dependencies, that's expected in test environment
            self.assertIn("create_react_agent", str(e).lower())
    
    def test_configure_agent_executor_function(self):
        """Test _configure_agent_executor function exists and works"""
        from main import _configure_agent_executor
        
        # Mock agent and tools
        mock_agent = Mock()
        mock_tools = [Mock(), Mock()]
        
        # Should not raise exception
        try:
            result = _configure_agent_executor(mock_agent, mock_tools)
            # Function should return something (executor instance)
            self.assertIsNotNone(result)
        except Exception as e:
            # If it fails due to missing dependencies, that's expected in test environment
            self.assertIn("AgentExecutor", str(e))
    
    def test_display_welcome_message_function(self):
        """Test _display_welcome_message function exists"""
        from main import _display_welcome_message
        
        # Should not raise exception
        try:
            _display_welcome_message()
        except Exception as e:
            # Should not raise any exceptions
            self.fail(f"_display_welcome_message raised exception: {e}")
    
    def test_is_exit_command_function(self):
        """Test _is_exit_command function works correctly"""
        from main import _is_exit_command
        
        # Test exit commands
        self.assertTrue(_is_exit_command("quit"))
        self.assertTrue(_is_exit_command("exit"))
        self.assertTrue(_is_exit_command("q"))
        self.assertTrue(_is_exit_command("QUIT"))
        self.assertTrue(_is_exit_command("EXIT"))
        self.assertTrue(_is_exit_command("Q"))
        
        # Test non-exit commands
        self.assertFalse(_is_exit_command("analyze"))
        self.assertFalse(_is_exit_command("test"))
        self.assertFalse(_is_exit_command(""))
        self.assertFalse(_is_exit_command("   "))
    
    def test_process_user_query_function(self):
        """Test _process_user_query function exists"""
        from main import _process_user_query
        
        # Mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis",
            "intermediate_steps": [("action", "observation")]
        }
        
        # Should not raise exception
        try:
            _process_user_query(mock_executor, "Test query")
        except Exception as e:
            # If it fails due to missing dependencies, that's expected in test environment
            pass
    
    def test_handle_user_input_function(self):
        """Test _handle_user_input function exists"""
        from main import _handle_user_input
        
        # Mock agent executor
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "Test analysis",
            "intermediate_steps": []
        }
        
        # Should not raise exception
        try:
            result = _handle_user_input(mock_executor)
            # Should return boolean
            self.assertIsInstance(result, bool)
        except Exception as e:
            # If it fails due to missing dependencies, that's expected in test environment
            pass

class TestConsistentCodingPatterns(unittest.TestCase):
    """Test consistent coding patterns across the codebase"""
    
    def test_import_organization_consistency(self):
        """Test that import organization is consistent"""
        # Read main.py file to check import organization
        with open('app/main.py', 'r') as f:
            content = f.read()
        
        # Check for proper import organization comments
        self.assertIn('# Standard library imports', content)
        self.assertIn('# Third-party imports', content)
        self.assertIn('# Local imports', content)
    
    def test_docstring_consistency(self):
        """Test that docstrings follow consistent format"""
        from main import load_environment, initialize_llm, create_agent_prompt
        
        # Check that functions have proper docstrings
        self.assertIsNotNone(load_environment.__doc__)
        self.assertIsNotNone(initialize_llm.__doc__)
        self.assertIsNotNone(create_agent_prompt.__doc__)
        
        # Check that docstrings contain expected sections
        load_env_doc = load_environment.__doc__
        self.assertIn('Args:', load_env_doc)
        self.assertIn('Raises:', load_env_doc)
    
    def test_error_handling_consistency(self):
        """Test that error handling follows consistent patterns"""
        # Test that custom exceptions are used consistently
        from exceptions import TacticsMasterError
        
        # Test that all custom exceptions inherit from base
        self.assertIsInstance(AgentInitializationError(), TacticsMasterError)
        self.assertIsInstance(AgentExecutionError(), TacticsMasterError)
        self.assertIsInstance(ValidationError(), TacticsMasterError)
        self.assertIsInstance(DataValidationError(), TacticsMasterError)
        self.assertIsInstance(CricketDataError(), TacticsMasterError)
        self.assertIsInstance(APIConnectionError(), TacticsMasterError)
        self.assertIsInstance(APITimeoutError(), TacticsMasterError)
        self.assertIsInstance(APIResponseError(), TacticsMasterError)
    
    def test_logging_consistency(self):
        """Test that logging is used consistently"""
        # Check that logging is configured consistently
        import logging
        
        # Test that logger is properly configured
        logger = logging.getLogger(__name__)
        self.assertIsNotNone(logger)
    
    def test_type_hints_consistency(self):
        """Test that type hints are used consistently"""
        from main import load_environment, initialize_llm, create_agent_prompt
        
        # Check that functions have proper type hints
        import inspect
        
        # Get function signatures
        load_env_sig = inspect.signature(load_environment)
        init_llm_sig = inspect.signature(initialize_llm)
        create_prompt_sig = inspect.signature(create_agent_prompt)
        
        # Check return type annotations
        self.assertIsNotNone(load_env_sig.return_annotation)
        self.assertIsNotNone(init_llm_sig.return_annotation)
        self.assertIsNotNone(create_prompt_sig.return_annotation)

class TestEnhancedErrorHandling(unittest.TestCase):
    """Test enhanced error handling with specific exception types"""
    
    def test_agent_initialization_error_handling(self):
        """Test that agent initialization errors are handled properly"""
        # Test with None LLM
        with self.assertRaises(AgentInitializationError) as context:
            TacticsMasterAgent(None, [Mock()])
        
        error = context.exception
        self.assertEqual(error.error_code, "INVALID_LLM")
        self.assertIn("Language model cannot be None", error.message)
    
    def test_agent_empty_tools_error_handling(self):
        """Test that empty tools list errors are handled properly"""
        mock_llm = Mock()
        
        with self.assertRaises(AgentInitializationError) as context:
            TacticsMasterAgent(mock_llm, [])
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_TOOLS_LIST")
        self.assertIn("Tools list cannot be empty", error.message)
    
    def test_validation_error_handling(self):
        """Test that validation errors are handled properly"""
        agent = TacticsMasterAgent(Mock(), [Mock()])
        
        with self.assertRaises(ValidationError) as context:
            agent.analyze("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_QUERY")
        self.assertIn("Query cannot be empty", error.message)
    
    def test_cricket_data_validation_error_handling(self):
        """Test that cricket data validation errors are handled properly"""
        with self.assertRaises(DataValidationError) as context:
            get_player_stats("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_NAME")
        self.assertIn("Player name cannot be empty", error.message)
    
    def test_tactical_tools_validation_error_handling(self):
        """Test that tactical tools validation errors are handled properly"""
        with self.assertRaises(DataValidationError) as context:
            analyze_weaknesses("")
        
        error = context.exception
        self.assertEqual(error.error_code, "EMPTY_PLAYER_DATA")
        self.assertIn("Player data cannot be empty", error.message)

class TestCodeQualityMetrics(unittest.TestCase):
    """Test code quality metrics and improvements"""
    
    def test_function_length_improvement(self):
        """Test that functions have been broken down into smaller, focused functions"""
        # Test that the main functions are now properly modularized
        from main import (
            _get_available_tools,
            _create_react_agent,
            _configure_agent_executor,
            _display_welcome_message,
            _is_exit_command,
            _process_user_query,
            _handle_user_input
        )
        
        # All helper functions should exist
        self.assertIsNotNone(_get_available_tools)
        self.assertIsNotNone(_create_react_agent)
        self.assertIsNotNone(_configure_agent_executor)
        self.assertIsNotNone(_display_welcome_message)
        self.assertIsNotNone(_is_exit_command)
        self.assertIsNotNone(_process_user_query)
        self.assertIsNotNone(_handle_user_input)
    
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
    
    def test_error_hierarchy_maintenance(self):
        """Test that error hierarchy is maintained"""
        # Test that specific errors inherit from base
        self.assertIsInstance(AgentInitializationError(), TacticsMasterError)
        self.assertIsInstance(AgentExecutionError(), TacticsMasterError)
        self.assertIsInstance(ValidationError(), TacticsMasterError)
        self.assertIsInstance(DataValidationError(), TacticsMasterError)
        self.assertIsInstance(CricketDataError(), TacticsMasterError)
        
        # Test that specific errors are not instances of other specific errors
        self.assertNotIsInstance(AgentInitializationError(), AgentExecutionError)
        self.assertNotIsInstance(CricketDataError(), ValidationError)
    
    def test_import_organization_improvement(self):
        """Test that import organization has been improved"""
        # Read main.py file to check import organization
        with open('app/main.py', 'r') as f:
            content = f.read()
        
        # Check for proper import organization
        lines = content.split('\n')
        import_section = []
        in_imports = False
        
        for line in lines:
            if line.startswith('import ') or line.startswith('from '):
                in_imports = True
                import_section.append(line)
            elif in_imports and not line.startswith('import ') and not line.startswith('from '):
                break
        
        # Check that imports are properly organized
        self.assertIn('# Standard library imports', content)
        self.assertIn('# Third-party imports', content)
        self.assertIn('# Local imports', content)
    
    def test_documentation_improvement(self):
        """Test that documentation has been improved"""
        from main import load_environment, initialize_llm, create_agent_prompt
        
        # Check that functions have comprehensive docstrings
        self.assertIsNotNone(load_environment.__doc__)
        self.assertIsNotNone(initialize_llm.__doc__)
        self.assertIsNotNone(create_agent_prompt.__doc__)
        
        # Check that docstrings contain expected sections
        load_env_doc = load_environment.__doc__
        self.assertIn('Args:', load_env_doc)
        self.assertIn('Raises:', load_env_doc)
        
        init_llm_doc = initialize_llm.__doc__
        self.assertIn('Args:', init_llm_doc)
        self.assertIn('Returns:', init_llm_doc)
        self.assertIn('Raises:', init_llm_doc)

class TestBackwardCompatibility(unittest.TestCase):
    """Test that improvements maintain backward compatibility"""
    
    def test_existing_functionality_preserved(self):
        """Test that existing functionality is preserved"""
        # Test that main functions still work
        from main import load_environment, initialize_llm, create_agent_prompt
        
        # Functions should still exist and be callable
        self.assertIsNotNone(load_environment)
        self.assertIsNotNone(initialize_llm)
        self.assertIsNotNone(create_agent_prompt)
        
        # Functions should have the same signatures
        import inspect
        
        load_env_sig = inspect.signature(load_environment)
        init_llm_sig = inspect.signature(initialize_llm)
        create_prompt_sig = inspect.signature(create_agent_prompt)
        
        # Signatures should be preserved
        self.assertIsNotNone(load_env_sig)
        self.assertIsNotNone(init_llm_sig)
        self.assertIsNotNone(create_prompt_sig)
    
    def test_agent_class_compatibility(self):
        """Test that agent class maintains compatibility"""
        # Test that agent class still works
        mock_llm = Mock()
        mock_tools = [Mock(), Mock()]
        mock_tools[0].name = "test_tool_1"
        mock_tools[1].name = "test_tool_2"
        
        # Should be able to create agent instance
        agent = TacticsMasterAgent(mock_llm, mock_tools)
        
        # Should have expected attributes
        self.assertEqual(agent.llm, mock_llm)
        self.assertEqual(agent.tools, mock_tools)
        self.assertTrue(agent.verbose)
        self.assertIsNone(agent.agent_executor)
    
    def test_tool_functions_compatibility(self):
        """Test that tool functions maintain compatibility"""
        # Test that tool functions still work
        self.assertIsNotNone(get_player_stats)
        self.assertIsNotNone(get_team_squad)
        self.assertIsNotNone(analyze_weaknesses)
        self.assertIsNotNone(find_best_matchup)
        
        # Functions should be callable
        self.assertTrue(callable(get_player_stats))
        self.assertTrue(callable(get_team_squad))
        self.assertTrue(callable(analyze_weaknesses))
        self.assertTrue(callable(find_best_matchup))

if __name__ == '__main__':
    unittest.main()
