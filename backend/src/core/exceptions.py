"""
Enhanced Exception Classes for Tactics Master System

This module provides a comprehensive set of custom exceptions with
structured error information, error codes, and context for better
error handling and debugging.
"""

from typing import Optional, Dict, Any, Union
from enum import Enum


class ErrorCode(Enum):
    """Standardized error codes for the application."""
    
    # Agent errors
    AGENT_INITIALIZATION_FAILED = "AGENT_INIT_FAILED"
    AGENT_EXECUTION_FAILED = "AGENT_EXEC_FAILED"
    AGENT_TOOL_ERROR = "AGENT_TOOL_ERROR"
    
    # API errors
    API_CONNECTION_FAILED = "API_CONN_FAILED"
    API_TIMEOUT = "API_TIMEOUT"
    API_RATE_LIMIT = "API_RATE_LIMIT"
    API_INVALID_RESPONSE = "API_INVALID_RESP"
    
    # Data errors
    DATA_VALIDATION_FAILED = "DATA_VALIDATION_FAILED"
    DATA_PROCESSING_FAILED = "DATA_PROC_FAILED"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    
    # Configuration errors
    CONFIG_MISSING = "CONFIG_MISSING"
    CONFIG_INVALID = "CONFIG_INVALID"
    
    # Authentication errors
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_INSUFFICIENT_PERMISSIONS = "AUTH_INSUFFICIENT_PERMS"
    
    # Business logic errors
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    QUERY_INVALID = "QUERY_INVALID"
    CONTEXT_INVALID = "CONTEXT_INVALID"
    
    # System errors
    SYSTEM_OVERLOAD = "SYSTEM_OVERLOAD"
    SYSTEM_MAINTENANCE = "SYSTEM_MAINTENANCE"
    SYSTEM_ERROR = "SYSTEM_ERROR"


class TacticsMasterError(Exception):
    """
    Base exception class for all Tactics Master related errors.
    
    This class provides structured error information including error codes,
    context, and additional metadata for better error handling and debugging.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[Union[ErrorCode, str]] = None,
        context: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None
    ):
        """
        Initialize the exception with structured error information.
        
        Args:
            message: Human-readable error message
            error_code: Standardized error code
            context: Additional context information
            details: Technical details for debugging
            retry_after: Seconds to wait before retrying (if applicable)
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code.value if isinstance(error_code, ErrorCode) else error_code
        self.context = context or {}
        self.details = details or {}
        self.retry_after = retry_after
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": self.message,
            "error_code": self.error_code,
            "context": self.context,
            "details": self.details,
            "retry_after": self.retry_after
        }


class AgentError(TacticsMasterError):
    """Base class for agent-related errors."""
    pass


class AgentInitializationError(AgentError):
    """Raised when agent initialization fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.AGENT_INITIALIZATION_FAILED,
            **kwargs
        )


class AgentExecutionError(AgentError):
    """Raised when agent execution fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.AGENT_EXECUTION_FAILED,
            **kwargs
        )


class ToolExecutionError(AgentError):
    """Raised when tool execution fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.AGENT_TOOL_ERROR,
            **kwargs
        )


class APIError(TacticsMasterError):
    """Base class for API-related errors."""
    pass


class APIConnectionError(APIError):
    """Raised when API connection fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.API_CONNECTION_FAILED,
            **kwargs
        )


class APITimeoutError(APIError):
    """Raised when API requests timeout."""
    
    def __init__(self, message: str, timeout: Optional[int] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.API_TIMEOUT,
            context={"timeout": timeout} if timeout else None,
            **kwargs
        )


class APIRateLimitError(APIError):
    """Raised when API rate limits are exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.API_RATE_LIMIT,
            retry_after=retry_after,
            **kwargs
        )


class APIResponseError(APIError):
    """Raised when API returns invalid response."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.API_INVALID_RESPONSE,
            context={"status_code": status_code} if status_code else None,
            **kwargs
        )


class DataError(TacticsMasterError):
    """Base class for data-related errors."""
    pass


class DataValidationError(DataError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, validation_errors: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.DATA_VALIDATION_FAILED,
            details={"validation_errors": validation_errors} if validation_errors else None,
            **kwargs
        )


class DataProcessingError(DataError):
    """Raised when data processing fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.DATA_PROCESSING_FAILED,
            **kwargs
        )


class DataNotFoundError(DataError):
    """Raised when requested data is not found."""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.DATA_NOT_FOUND,
            context={"resource_type": resource_type} if resource_type else None,
            **kwargs
        )


class ConfigurationError(TacticsMasterError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.CONFIG_MISSING,
            context={"config_key": config_key} if config_key else None,
            **kwargs
        )


class AuthenticationError(TacticsMasterError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.AUTH_TOKEN_INVALID,
            **kwargs
        )


class BusinessLogicError(TacticsMasterError):
    """Base class for business logic errors."""
    pass


class AnalysisError(BusinessLogicError):
    """Raised when analysis operations fail."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.ANALYSIS_FAILED,
            **kwargs
        )


class QueryValidationError(BusinessLogicError):
    """Raised when query validation fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.QUERY_INVALID,
            **kwargs
        )


class SystemError(TacticsMasterError):
    """Base class for system-level errors."""
    pass


class SystemOverloadError(SystemError):
    """Raised when system is overloaded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.SYSTEM_OVERLOAD,
            retry_after=retry_after,
            **kwargs
        )


class ServiceUnavailableError(SystemError):
    """Raised when services are unavailable."""
    
    def __init__(self, message: str, service: Optional[str] = None, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.SYSTEM_MAINTENANCE,
            context={"service": service} if service else None,
            **kwargs
        )


# Legacy exception classes for backward compatibility
class CricketDataError(DataError):
    """Legacy: Raised when cricket data operations fail."""
    pass


class NetworkError(APIError):
    """Legacy: Raised when network operations fail."""
    pass


class RateLimitError(APIRateLimitError):
    """Legacy: Raised when rate limits are exceeded."""
    pass


class ValidationError(DataValidationError):
    """Legacy: Raised when input validation fails."""
    pass
