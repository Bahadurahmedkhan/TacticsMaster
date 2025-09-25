"""
Core package for Tactics Master Backend

This package contains core functionality including exceptions,
middleware, dependencies, and base classes.
"""

from .exceptions import (
    TacticsMasterError,
    AgentError,
    AgentInitializationError,
    AgentExecutionError,
    ToolExecutionError,
    APIError,
    APIConnectionError,
    APITimeoutError,
    APIRateLimitError,
    APIResponseError,
    DataError,
    DataValidationError,
    DataProcessingError,
    DataNotFoundError,
    ConfigurationError,
    AuthenticationError,
    BusinessLogicError,
    AnalysisError,
    QueryValidationError,
    SystemError,
    SystemOverloadError,
    ServiceUnavailableError,
    # Legacy exceptions
    CricketDataError,
    NetworkError,
    RateLimitError,
    ValidationError,
    ErrorCode
)

__all__ = [
    "TacticsMasterError",
    "AgentError",
    "AgentInitializationError", 
    "AgentExecutionError",
    "ToolExecutionError",
    "APIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIRateLimitError",
    "APIResponseError",
    "DataError",
    "DataValidationError",
    "DataProcessingError",
    "DataNotFoundError",
    "ConfigurationError",
    "AuthenticationError",
    "BusinessLogicError",
    "AnalysisError",
    "QueryValidationError",
    "SystemError",
    "SystemOverloadError",
    "ServiceUnavailableError",
    # Legacy exceptions
    "CricketDataError",
    "NetworkError", 
    "RateLimitError",
    "ValidationError",
    "ErrorCode"
]
