"""
Custom Exception Classes for Tactics Master System

This module defines specific exception types for better error handling
and more precise error reporting throughout the application.

Author: Tactics Master Team
Version: 1.0.0
"""

from typing import Optional, Dict, Any


class TacticsMasterError(Exception):
    """Base exception class for all Tactics Master related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}


class AgentInitializationError(TacticsMasterError):
    """Raised when agent initialization fails."""
    pass


class AgentExecutionError(TacticsMasterError):
    """Raised when agent execution fails."""
    pass


class ToolExecutionError(TacticsMasterError):
    """Raised when tool execution fails."""
    pass


class CricketDataError(TacticsMasterError):
    """Raised when cricket data operations fail."""
    pass


class APIConnectionError(TacticsMasterError):
    """Raised when API connection fails."""
    pass


class APITimeoutError(TacticsMasterError):
    """Raised when API requests timeout."""
    pass


class APIResponseError(TacticsMasterError):
    """Raised when API returns invalid response."""
    pass


class DataValidationError(TacticsMasterError):
    """Raised when data validation fails."""
    pass


class ConfigurationError(TacticsMasterError):
    """Raised when configuration is invalid or missing."""
    pass


class AnalysisError(TacticsMasterError):
    """Raised when analysis operations fail."""
    pass


class NetworkError(TacticsMasterError):
    """Raised when network operations fail."""
    pass


class AuthenticationError(TacticsMasterError):
    """Raised when authentication fails."""
    pass


class RateLimitError(TacticsMasterError):
    """Raised when API rate limits are exceeded."""
    pass


class DataProcessingError(TacticsMasterError):
    """Raised when data processing operations fail."""
    pass


class ValidationError(TacticsMasterError):
    """Raised when input validation fails."""
    pass


class ServiceUnavailableError(TacticsMasterError):
    """Raised when external services are unavailable."""
    pass
