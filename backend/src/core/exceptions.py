"""
Enhanced Exception Classes for Tactics Master System

This module provides comprehensive exception handling with detailed error tracking,
contextual information, and proper error categorization for better debugging
and user experience.

Author: Tactics Master Team
Version: 2.0.0
"""

import traceback
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better classification"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NETWORK = "network"
    API = "api"
    DATA = "data"
    PROCESSING = "processing"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"


class TacticsMasterError(Exception):
    """
    Enhanced base exception class for all Tactics Master related errors.
    
    Provides comprehensive error tracking with context, severity, and categorization.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        original_error: Optional[Exception] = None,
        user_message: Optional[str] = None,
        retry_after: Optional[int] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}
        self.severity = severity
        self.category = category
        self.original_error = original_error
        self.user_message = user_message or message
        self.retry_after = retry_after
        self.timestamp = datetime.now().isoformat()
        self.traceback = traceback.format_exc()
        
        # Log the error
        self._log_error()
    
    def _log_error(self) -> None:
        """Log the error with appropriate level based on severity"""
        logger = logging.getLogger(__name__)
        
        log_message = f"[{self.error_code}] {self.message}"
        if self.context:
            log_message += f" | Context: {self.context}"
        if self.original_error:
            log_message += f" | Original: {str(self.original_error)}"
        
        if self.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif self.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif self.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "user_message": self.user_message,
            "severity": self.severity.value,
            "category": self.category.value,
            "context": self.context,
            "timestamp": self.timestamp,
            "retry_after": self.retry_after
        }
    
    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


# Agent-related exceptions
class AgentInitializationError(TacticsMasterError):
    """Raised when agent initialization fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.SYSTEM,
            **kwargs
        )


class AgentExecutionError(TacticsMasterError):
    """Raised when agent execution fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            **kwargs
        )


class ToolExecutionError(TacticsMasterError):
    """Raised when tool execution fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.PROCESSING,
            **kwargs
        )


# Data-related exceptions
class CricketDataError(TacticsMasterError):
    """Raised when cricket data operations fail"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.DATA,
            **kwargs
        )


class DataValidationError(TacticsMasterError):
    """Raised when data validation fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            **kwargs
        )


class DataProcessingError(TacticsMasterError):
    """Raised when data processing operations fail"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.PROCESSING,
            **kwargs
        )


# API-related exceptions
class APIConnectionError(TacticsMasterError):
    """Raised when API connection fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.NETWORK,
            user_message="Unable to connect to cricket data services. Please try again later.",
            **kwargs
        )


class APITimeoutError(TacticsMasterError):
    """Raised when API requests timeout"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.NETWORK,
            user_message="Request timed out. Please try again.",
            retry_after=30,
            **kwargs
        )


class APIResponseError(TacticsMasterError):
    """Raised when API returns invalid response"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.API,
            **kwargs
        )


class RateLimitError(TacticsMasterError):
    """Raised when API rate limits are exceeded"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.API,
            user_message="Too many requests. Please wait before trying again.",
            retry_after=60,
            **kwargs
        )


# Authentication and Authorization
class AuthenticationError(TacticsMasterError):
    """Raised when authentication fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.AUTHENTICATION,
            user_message="Authentication failed. Please check your credentials.",
            **kwargs
        )


class AuthorizationError(TacticsMasterError):
    """Raised when authorization fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.AUTHORIZATION,
            user_message="You don't have permission to perform this action.",
            **kwargs
        )


# Configuration and System
class ConfigurationError(TacticsMasterError):
    """Raised when configuration is invalid or missing"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.CONFIGURATION,
            **kwargs
        )


class ServiceUnavailableError(TacticsMasterError):
    """Raised when external services are unavailable"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.SYSTEM,
            user_message="Service temporarily unavailable. Please try again later.",
            **kwargs
        )


class NetworkError(TacticsMasterError):
    """Raised when network operations fail"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.NETWORK,
            user_message="Network error. Please check your connection and try again.",
            **kwargs
        )


# Business Logic
class AnalysisError(TacticsMasterError):
    """Raised when analysis operations fail"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            **kwargs
        )


class ValidationError(TacticsMasterError):
    """Raised when input validation fails"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            **kwargs
        )


# Error Handler Utilities
class ErrorHandler:
    """Utility class for handling and formatting errors"""
    
    @staticmethod
    def handle_exception(
        exception: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None
    ) -> TacticsMasterError:
        """
        Convert any exception to a TacticsMasterError with proper context.
        
        Args:
            exception: The original exception
            context: Additional context information
            user_message: User-friendly error message
            
        Returns:
            TacticsMasterError: Properly formatted error
        """
        if isinstance(exception, TacticsMasterError):
            return exception
        
        # Convert common exceptions to appropriate TacticsMasterError types
        if isinstance(exception, ConnectionError):
            return APIConnectionError(
                message=str(exception),
                original_error=exception,
                context=context,
                user_message=user_message
            )
        elif isinstance(exception, TimeoutError):
            return APITimeoutError(
                message=str(exception),
                original_error=exception,
                context=context,
                user_message=user_message
            )
        elif isinstance(exception, ValueError):
            return ValidationError(
                message=str(exception),
                original_error=exception,
                context=context,
                user_message=user_message
            )
        else:
            return TacticsMasterError(
                message=str(exception),
                original_error=exception,
                context=context,
                user_message=user_message or "An unexpected error occurred"
            )
    
    @staticmethod
    def format_error_response(error: TacticsMasterError) -> Dict[str, Any]:
        """
        Format error for API response.
        
        Args:
            error: The error to format
            
        Returns:
            Dict containing formatted error information
        """
        response = error.to_dict()
        
        # Add HTTP status code based on error type
        if isinstance(error, ValidationError):
            response["status_code"] = 400
        elif isinstance(error, AuthenticationError):
            response["status_code"] = 401
        elif isinstance(error, AuthorizationError):
            response["status_code"] = 403
        elif isinstance(error, APIConnectionError):
            response["status_code"] = 503
        elif isinstance(error, RateLimitError):
            response["status_code"] = 429
        else:
            response["status_code"] = 500
        
        return response