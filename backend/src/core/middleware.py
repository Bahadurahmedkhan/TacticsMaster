"""
Enhanced Middleware System for Tactics Master

This module provides comprehensive middleware for request processing, error handling,
logging, and performance monitoring.

Author: Tactics Master Team
Version: 2.0.0
"""

import time
import json
import logging
from typing import Callable, Dict, Any, Optional
from datetime import datetime
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp

from .exceptions import TacticsMasterError, ErrorHandler
from .logging import RequestLogger, PerformanceLogger
from ..config.settings import get_settings


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive error handling and response formatting.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("backend.middleware.error")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Handle requests with comprehensive error handling"""
        try:
            response = await call_next(request)
            return response
        
        except HTTPException as e:
            self.logger.warning(f"HTTP Exception: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": True,
                    "message": e.detail,
                    "status_code": e.status_code,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        except TacticsMasterError as e:
            self.logger.error(f"Tactics Master Error: {e.error_code} - {e.message}")
            error_response = ErrorHandler.format_error_response(e)
            return JSONResponse(
                status_code=error_response.get("status_code", 500),
                content={
                    "error": True,
                    **error_response
                }
            )
        
        except Exception as e:
            self.logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            
            # Convert to TacticsMasterError
            tactics_error = ErrorHandler.handle_exception(
                e,
                context={"path": request.url.path, "method": request.method},
                user_message="An unexpected error occurred"
            )
            
            error_response = ErrorHandler.format_error_response(tactics_error)
            return JSONResponse(
                status_code=error_response.get("status_code", 500),
                content={
                    "error": True,
                    **error_response
                }
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive request/response logging.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_logger = RequestLogger()
        self.logger = logging.getLogger("backend.middleware.logging")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Log requests and responses"""
        start_time = time.time()
        
        # Extract request information
        request_id = request.headers.get("X-Request-ID", "unknown")
        user_id = getattr(request.state, "user_id", None)
        
        # Log request
        self.logger.info(f"Request started: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            self.request_logger.log_request(
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration=duration,
                user_id=user_id,
                request_id=request_id
            )
            
            # Add response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            
            return response
        
        except Exception as e:
            duration = time.time() - start_time
            
            # Log error
            self.logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
            
            # Re-raise to be handled by error middleware
            raise


class PerformanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware for performance monitoring and metrics collection.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.performance_logger = PerformanceLogger()
        self.logger = logging.getLogger("backend.middleware.performance")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Monitor request performance"""
        operation = f"{request.method}_{request.url.path.replace('/', '_')}"
        
        # Start performance monitoring
        self.performance_logger.start_timer(operation)
        
        try:
            response = await call_next(request)
            
            # Log performance metrics
            duration = self.performance_logger.end_timer(operation)
            
            # Log slow requests
            if duration > 5.0:  # 5 seconds threshold
                self.logger.warning(f"Slow request detected: {operation} took {duration:.3f}s")
            
            # Add performance headers
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            
            return response
        
        except Exception as e:
            # End timer even on error
            self.performance_logger.end_timer(operation, logging.ERROR)
            raise


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware for security headers and protection.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.settings = get_settings()
        self.logger = logging.getLogger("backend.middleware.security")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Add security headers and perform security checks"""
        if not self.settings.security.enable_security_headers:
            return await call_next(request)
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy
        if self.settings.security.content_security_policy:
            response.headers["Content-Security-Policy"] = self.settings.security.content_security_policy
        
        # Strict Transport Security (HTTPS only)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting and request throttling.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.settings = get_settings()
        self.logger = logging.getLogger("backend.middleware.ratelimit")
        self._request_counts: Dict[str, Dict[str, Any]] = {}
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Apply rate limiting"""
        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        user_id = getattr(request.state, "user_id", None)
        identifier = user_id or client_ip
        
        # Check rate limit
        if self._is_rate_limited(identifier):
            self.logger.warning(f"Rate limit exceeded for {identifier}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": True,
                    "message": "Rate limit exceeded",
                    "retry_after": self.settings.api.rate_limit_window,
                    "timestamp": datetime.now().isoformat()
                },
                headers={"Retry-After": str(self.settings.api.rate_limit_window)}
            )
        
        # Record request
        self._record_request(identifier)
        
        response = await call_next(request)
        return response
    
    def _is_rate_limited(self, identifier: str) -> bool:
        """Check if identifier is rate limited"""
        current_time = time.time()
        window_start = current_time - self.settings.api.rate_limit_window
        
        # Clean old entries
        if identifier in self._request_counts:
            self._request_counts[identifier] = {
                timestamp: count for timestamp, count in self._request_counts[identifier].items()
                if timestamp > window_start
            }
        
        # Count requests in window
        if identifier in self._request_counts:
            request_count = sum(self._request_counts[identifier].values())
        else:
            request_count = 0
        
        return request_count >= self.settings.api.rate_limit_requests
    
    def _record_request(self, identifier: str) -> None:
        """Record a request for rate limiting"""
        current_time = time.time()
        
        if identifier not in self._request_counts:
            self._request_counts[identifier] = {}
        
        if current_time not in self._request_counts[identifier]:
            self._request_counts[identifier][current_time] = 0
        
        self._request_counts[identifier][current_time] += 1


class CORSMiddleware(BaseHTTPMiddleware):
    """
    Enhanced CORS middleware with environment-specific configuration.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.settings = get_settings()
        self.logger = logging.getLogger("backend.middleware.cors")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Handle CORS headers"""
        response = await call_next(request)
        
        # Get allowed origins based on environment
        allowed_origins = self.settings.get_cors_origins()
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            if origin and (origin in allowed_origins or "*" in allowed_origins):
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = ", ".join(self.settings.security.cors_methods)
                response.headers["Access-Control-Allow-Headers"] = ", ".join(self.settings.security.cors_headers)
                response.headers["Access-Control-Max-Age"] = "86400"
        
        # Add CORS headers to all responses
        origin = request.headers.get("Origin")
        if origin and (origin in allowed_origins or "*" in allowed_origins):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request ID generation and tracking.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("backend.middleware.request_id")
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Generate and track request IDs"""
        import uuid
        
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Store in request state
        request.state.request_id = request_id
        
        # Add to response headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


class MiddlewareManager:
    """
    Manager for configuring and applying middleware.
    """
    
    @staticmethod
    def setup_middleware(app: ASGIApp) -> ASGIApp:
        """
        Setup all middleware for the application.
        
        Args:
            app: FastAPI application instance
            
        Returns:
            ASGIApp: Application with middleware configured
        """
        # Add middleware in reverse order (last added is first executed)
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(CORSMiddleware)
        app.add_middleware(RateLimitMiddleware)
        app.add_middleware(SecurityMiddleware)
        app.add_middleware(PerformanceMiddleware)
        app.add_middleware(LoggingMiddleware)
        app.add_middleware(ErrorHandlingMiddleware)
        
        return app
