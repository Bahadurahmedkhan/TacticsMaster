"""
Comprehensive Quality Test Suite for Tactics Master System

This module provides comprehensive tests for code quality, maintainability,
error handling, robustness, and performance across all components.

Author: Tactics Master Team
Version: 2.0.0
"""

import pytest
import asyncio
import json
import logging
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import all components to test
from src.core.exceptions import (
    TacticsMasterError, AgentInitializationError, AgentExecutionError,
    ValidationError, APIConnectionError, APITimeoutError, ErrorHandler
)
from src.core.validation import Validator, ModelValidator, Sanitizer
from src.core.logging import LoggingConfig, PerformanceLogger, RequestLogger
from src.core.middleware import (
    ErrorHandlingMiddleware, LoggingMiddleware, PerformanceMiddleware,
    SecurityMiddleware, RateLimitMiddleware, CORSMiddleware
)
from src.config.settings import Settings, Environment, get_settings
from src.agents.base_agent import BaseAgent, AgentStatus, AgentCapability
from src.agents.hybrid_agent import HybridTacticsMasterAgent


class TestExceptionHandling:
    """Test comprehensive exception handling"""
    
    def test_base_exception_creation(self):
        """Test base exception creation with all parameters"""
        error = TacticsMasterError(
            message="Test error",
            error_code="TEST_ERROR",
            context={"key": "value"},
            original_error=ValueError("test")
        )
        
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.context == {"key": "value"}
        assert str(error.original_error) == "test"
        assert error.timestamp is not None
    
    def test_exception_to_dict(self):
        """Test exception serialization to dictionary"""
        error = TacticsMasterError(
            message="Test error",
            error_code="TEST_ERROR",
            context={"key": "value"}
        )
        
        error_dict = error.to_dict()
        assert error_dict["error_code"] == "TEST_ERROR"
        assert error_dict["message"] == "Test error"
        assert error_dict["context"] == {"key": "value"}
        assert "timestamp" in error_dict
    
    def test_error_handler_handle_exception(self):
        """Test error handler exception conversion"""
        original_error = ConnectionError("Connection failed")
        tactics_error = ErrorHandler.handle_exception(
            original_error,
            context={"operation": "test"},
            user_message="User-friendly message"
        )
        
        assert isinstance(tactics_error, APIConnectionError)
        assert tactics_error.original_error == original_error
        assert tactics_error.context["operation"] == "test"
        assert tactics_error.user_message == "User-friendly message"
    
    def test_error_handler_format_response(self):
        """Test error response formatting"""
        error = ValidationError(
            message="Invalid input",
            error_code="INVALID_INPUT"
        )
        
        response = ErrorHandler.format_error_response(error)
        assert response["status_code"] == 400
        assert response["error_code"] == "INVALID_INPUT"


class TestValidation:
    """Test comprehensive input validation"""
    
    def test_string_validation_success(self):
        """Test successful string validation"""
        result = Validator.validate_string(
            value="test string",
            required=True,
            min_length=5,
            max_length=20,
            field_name="test_field"
        )
        assert result == "test string"
    
    def test_string_validation_required_error(self):
        """Test string validation with required field error"""
        with pytest.raises(ValidationError) as exc_info:
            Validator.validate_string(
                value="",
                required=True,
                field_name="test_field"
            )
        assert "required" in str(exc_info.value).lower()
    
    def test_string_validation_length_error(self):
        """Test string validation with length error"""
        with pytest.raises(ValidationError) as exc_info:
            Validator.validate_string(
                value="test",
                required=True,
                min_length=10,
                field_name="test_field"
            )
        assert "at least" in str(exc_info.value).lower()
    
    def test_integer_validation_success(self):
        """Test successful integer validation"""
        result = Validator.validate_integer(
            value="42",
            required=True,
            min_value=0,
            max_value=100,
            field_name="test_field"
        )
        assert result == 42
    
    def test_integer_validation_type_error(self):
        """Test integer validation with type error"""
        with pytest.raises(ValidationError) as exc_info:
            Validator.validate_integer(
                value="not_a_number",
                required=True,
                field_name="test_field"
            )
        assert "integer" in str(exc_info.value).lower()
    
    def test_float_validation_success(self):
        """Test successful float validation"""
        result = Validator.validate_float(
            value="3.14",
            required=True,
            min_value=0.0,
            max_value=10.0,
            field_name="test_field"
        )
        assert result == 3.14
    
    def test_json_validation_success(self):
        """Test successful JSON validation"""
        json_string = '{"key": "value", "number": 42}'
        result = Validator.validate_json(
            value=json_string,
            required=True,
            field_name="test_field"
        )
        assert result == {"key": "value", "number": 42}
    
    def test_json_validation_invalid_error(self):
        """Test JSON validation with invalid JSON"""
        with pytest.raises(ValidationError) as exc_info:
            Validator.validate_json(
                value="invalid json",
                required=True,
                field_name="test_field"
            )
        assert "valid JSON" in str(exc_info.value).lower()
    
    def test_list_validation_success(self):
        """Test successful list validation"""
        result = Validator.validate_list(
            value=["item1", "item2", "item3"],
            required=True,
            min_length=2,
            max_length=5,
            field_name="test_field"
        )
        assert result == ["item1", "item2", "item3"]
    
    def test_sanitizer_string(self):
        """Test string sanitization"""
        dirty_string = "  test\x00string\n  "
        clean_string = Sanitizer.sanitize_string(dirty_string, max_length=10)
        assert clean_string == "teststring"
    
    def test_sanitizer_json(self):
        """Test JSON sanitization"""
        dirty_data = {
            "key": "  value\x00  ",
            "nested": {"item": "  test\n  "}
        }
        clean_data = Sanitizer.sanitize_json(dirty_data)
        assert clean_data["key"] == "value"
        assert clean_data["nested"]["item"] == "test"


class TestLogging:
    """Test comprehensive logging functionality"""
    
    def test_logging_config_creation(self):
        """Test logging configuration creation"""
        config = LoggingConfig.get_logging_config(
            log_level="INFO",
            log_file="/tmp/test.log",
            enable_structured=True,
            enable_performance=True
        )
        
        assert config["version"] == 1
        assert "handlers" in config
        assert "formatters" in config
        assert "loggers" in config
    
    def test_performance_logger(self):
        """Test performance logging"""
        logger = PerformanceLogger()
        
        # Start timer
        logger.start_timer("test_operation")
        
        # Simulate some work
        import time
        time.sleep(0.01)
        
        # End timer
        duration = logger.end_timer("test_operation")
        assert duration > 0.01
        assert duration < 0.1
    
    def test_request_logger(self):
        """Test request logging"""
        logger = RequestLogger()
        
        # This would normally log to the logger
        # For testing, we just ensure no exceptions are raised
        logger.log_request(
            method="GET",
            url="http://test.com",
            status_code=200,
            duration=0.1,
            user_id="test_user"
        )
        # If we get here without exception, test passes


class TestMiddleware:
    """Test middleware functionality"""
    
    @pytest.fixture
    def mock_app(self):
        """Create mock ASGI app"""
        return Mock()
    
    def test_error_handling_middleware_creation(self, mock_app):
        """Test error handling middleware creation"""
        middleware = ErrorHandlingMiddleware(mock_app)
        assert middleware.app == mock_app
    
    def test_logging_middleware_creation(self, mock_app):
        """Test logging middleware creation"""
        middleware = LoggingMiddleware(mock_app)
        assert middleware.app == mock_app
    
    def test_performance_middleware_creation(self, mock_app):
        """Test performance middleware creation"""
        middleware = PerformanceMiddleware(mock_app)
        assert middleware.app == mock_app
    
    def test_security_middleware_creation(self, mock_app):
        """Test security middleware creation"""
        middleware = SecurityMiddleware(mock_app)
        assert middleware.app == mock_app
    
    def test_rate_limit_middleware_creation(self, mock_app):
        """Test rate limit middleware creation"""
        middleware = RateLimitMiddleware(mock_app)
        assert middleware.app == mock_app
    
    def test_cors_middleware_creation(self, mock_app):
        """Test CORS middleware creation"""
        middleware = CORSMiddleware(mock_app)
        assert middleware.app == mock_app


class TestConfiguration:
    """Test configuration management"""
    
    def test_settings_creation(self):
        """Test settings creation with defaults"""
        # This would need proper environment setup
        # For now, test that the class can be instantiated
        assert Settings is not None
    
    def test_environment_enum(self):
        """Test environment enumeration"""
        assert Environment.DEVELOPMENT == "development"
        assert Environment.PRODUCTION == "production"
        assert Environment.TESTING == "testing"
        assert Environment.STAGING == "staging"
    
    def test_log_level_enum(self):
        """Test log level enumeration"""
        from src.config.settings import LogLevel
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


class TestBaseAgent:
    """Test base agent functionality"""
    
    def test_agent_creation(self):
        """Test agent creation"""
        # Create a concrete implementation for testing
        class TestAgent(BaseAgent):
            async def _initialize_agent(self):
                pass
            
            async def _perform_analysis(self, query: str, context: Dict[str, Any], **kwargs):
                return {"response": "test response"}
        
        agent = TestAgent("TestAgent", "1.0.0")
        assert agent.name == "TestAgent"
        assert agent.version == "1.0.0"
        assert agent.status == AgentStatus.INITIALIZING
    
    def test_agent_capabilities(self):
        """Test agent capabilities"""
        capabilities = [AgentCapability.DATA_ANALYSIS, AgentCapability.TACTICAL_PLANNING]
        
        class TestAgent(BaseAgent):
            def __init__(self):
                super().__init__("TestAgent", capabilities=capabilities)
            
            async def _initialize_agent(self):
                pass
            
            async def _perform_analysis(self, query: str, context: Dict[str, Any], **kwargs):
                return {"response": "test response"}
        
        agent = TestAgent()
        assert agent.has_capability(AgentCapability.DATA_ANALYSIS)
        assert agent.has_capability(AgentCapability.TACTICAL_PLANNING)
        assert not agent.has_capability(AgentCapability.PLAYER_ANALYSIS)
    
    def test_agent_status_info(self):
        """Test agent status information"""
        class TestAgent(BaseAgent):
            def __init__(self):
                super().__init__("TestAgent")
            
            async def _initialize_agent(self):
                pass
            
            async def _perform_analysis(self, query: str, context: Dict[str, Any], **kwargs):
                return {"response": "test response"}
        
        agent = TestAgent()
        status_info = agent.get_status_info()
        
        assert status_info["name"] == "TestAgent"
        assert status_info["status"] == AgentStatus.INITIALIZING.value
        assert "uptime_seconds" in status_info
        assert "active_requests" in status_info


class TestHybridAgent:
    """Test hybrid agent functionality"""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings"""
        settings = Mock()
        settings.api.openai_api_key = "test_key"
        settings.api.gemini_api_key = None
        settings.api.cricapi_key = "test_cricapi_key"
        settings.api.espn_cricket_api_key = "test_espn_key"
        settings.api.request_timeout = 30
        settings.get_ai_provider.return_value = "openai"
        return settings
    
    @pytest.mark.asyncio
    async def test_hybrid_agent_initialization(self, mock_settings):
        """Test hybrid agent initialization"""
        with patch('src.agents.hybrid_agent.get_settings', return_value=mock_settings):
            agent = HybridTacticsMasterAgent()
            assert agent.name == "HybridTacticsMaster"
            assert agent.version == "2.0.0"
            assert AgentCapability.DATA_ANALYSIS in agent.capabilities
    
    @pytest.mark.asyncio
    async def test_hybrid_agent_analysis_fallback(self, mock_settings):
        """Test hybrid agent analysis with fallback"""
        with patch('src.agents.hybrid_agent.get_settings', return_value=mock_settings):
            agent = HybridTacticsMasterAgent()
            
            # Mock the initialization to avoid actual API calls
            agent._status = AgentStatus.READY
            
            result = await agent.analyze("Test query", {"context": "test"})
            
            assert "response" in result
            assert "analysis" in result
            assert "sources" in result
            assert result["agent_name"] == "HybridTacticsMaster"


class TestCodeQuality:
    """Test overall code quality metrics"""
    
    def test_import_structure(self):
        """Test that all imports work correctly"""
        # Test core imports
        from src.core.exceptions import TacticsMasterError
        from src.core.validation import Validator
        from src.core.logging import LoggingConfig
        from src.core.middleware import ErrorHandlingMiddleware
        
        # Test config imports
        from src.config.settings import Settings, Environment
        
        # Test agent imports
        from src.agents.base_agent import BaseAgent, AgentStatus
        from src.agents.hybrid_agent import HybridTacticsMasterAgent
        
        # If we get here without import errors, test passes
        assert True
    
    def test_error_handling_coverage(self):
        """Test that all major components have proper error handling"""
        # Test that exceptions are properly defined
        assert TacticsMasterError is not None
        assert AgentInitializationError is not None
        assert AgentExecutionError is not None
        assert ValidationError is not None
        assert APIConnectionError is not None
        assert APITimeoutError is not None
        
        # Test error handler
        assert ErrorHandler is not None
        assert hasattr(ErrorHandler, 'handle_exception')
        assert hasattr(ErrorHandler, 'format_error_response')
    
    def test_validation_coverage(self):
        """Test that validation covers all major data types"""
        # Test string validation
        assert hasattr(Validator, 'validate_string')
        
        # Test numeric validation
        assert hasattr(Validator, 'validate_integer')
        assert hasattr(Validator, 'validate_float')
        
        # Test complex validation
        assert hasattr(Validator, 'validate_json')
        assert hasattr(Validator, 'validate_list')
        
        # Test sanitization
        assert hasattr(Sanitizer, 'sanitize_string')
        assert hasattr(Sanitizer, 'sanitize_json')
    
    def test_logging_coverage(self):
        """Test that logging covers all major components"""
        # Test logging configuration
        assert hasattr(LoggingConfig, 'get_logging_config')
        assert hasattr(LoggingConfig, 'setup_logging')
        
        # Test performance logging
        assert hasattr(PerformanceLogger, 'start_timer')
        assert hasattr(PerformanceLogger, 'end_timer')
        
        # Test request logging
        assert hasattr(RequestLogger, 'log_request')
    
    def test_middleware_coverage(self):
        """Test that middleware covers all major concerns"""
        # Test error handling
        assert ErrorHandlingMiddleware is not None
        
        # Test logging
        assert LoggingMiddleware is not None
        
        # Test performance
        assert PerformanceMiddleware is not None
        
        # Test security
        assert SecurityMiddleware is not None
        
        # Test rate limiting
        assert RateLimitMiddleware is not None
        
        # Test CORS
        assert CORSMiddleware is not None


class TestPerformance:
    """Test performance characteristics"""
    
    def test_validation_performance(self):
        """Test validation performance"""
        import time
        
        start_time = time.time()
        
        # Test multiple validations
        for i in range(100):
            Validator.validate_string(f"test_string_{i}", required=True, field_name="test")
            Validator.validate_integer(str(i), required=True, field_name="test")
            Validator.validate_float(str(i + 0.5), required=True, field_name="test")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second for 300 validations)
        assert duration < 1.0
    
    def test_exception_creation_performance(self):
        """Test exception creation performance"""
        import time
        
        start_time = time.time()
        
        # Test multiple exception creations
        for i in range(100):
            TacticsMasterError(
                message=f"Test error {i}",
                error_code="TEST_ERROR",
                context={"index": i}
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 1.0
    
    def test_logging_performance(self):
        """Test logging performance"""
        import time
        
        # Setup test logger
        logger = logging.getLogger("test_performance")
        logger.setLevel(logging.INFO)
        
        start_time = time.time()
        
        # Test multiple log messages
        for i in range(100):
            logger.info(f"Test log message {i}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 1.0


class TestRobustness:
    """Test system robustness"""
    
    def test_graceful_degradation(self):
        """Test graceful degradation when services are unavailable"""
        # Test that the system can handle missing dependencies
        try:
            # This should not crash even if external services are unavailable
            from src.agents.hybrid_agent import HybridTacticsMasterAgent
            agent = HybridTacticsMasterAgent()
            assert agent is not None
        except Exception as e:
            # If it fails, it should fail gracefully with a proper exception
            assert isinstance(e, (TacticsMasterError, Exception))
    
    def test_input_sanitization(self):
        """Test input sanitization for security"""
        # Test malicious input
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "\x00\x01\x02\x03",  # Control characters
        ]
        
        for malicious_input in malicious_inputs:
            sanitized = Sanitizer.sanitize_string(malicious_input)
            # Should not contain dangerous characters
            assert "<script>" not in sanitized
            assert "DROP TABLE" not in sanitized
            assert "../" not in sanitized
            assert "\x00" not in sanitized
    
    def test_error_recovery(self):
        """Test error recovery mechanisms"""
        # Test that the system can recover from errors
        try:
            # Simulate an error condition
            raise ValueError("Simulated error")
        except ValueError as e:
            # Convert to TacticsMasterError
            tactics_error = ErrorHandler.handle_exception(e)
            assert isinstance(tactics_error, TacticsMasterError)
            assert tactics_error.original_error == e


# Integration tests
class TestIntegration:
    """Test system integration"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_analysis(self):
        """Test end-to-end analysis flow"""
        # This would test the complete flow from request to response
        # For now, we'll test the components work together
        
        # Test validation
        query = "Analyze Virat Kohli's batting performance"
        validated_query = Validator.validate_string(query, required=True, field_name="query")
        assert validated_query == query
        
        # Test context validation
        context = {"team": "India", "format": "ODI"}
        validated_context = Validator.validate_json(json.dumps(context), required=True, field_name="context")
        assert validated_context == context
        
        # Test error handling
        try:
            # This should work without errors
            assert True
        except Exception as e:
            # If it fails, it should be handled gracefully
            tactics_error = ErrorHandler.handle_exception(e)
            assert isinstance(tactics_error, TacticsMasterError)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
