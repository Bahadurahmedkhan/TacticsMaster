"""
Tactics Master - Main Application

This module provides the main FastAPI application with comprehensive
configuration, middleware, error handling, and API endpoints.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config.settings import get_settings, Environment
from .core.exceptions import TacticsMasterError, ErrorHandler
from .core.middleware import MiddlewareManager
from .core.logging import LoggingConfig, initialize_logging
from .core.dependencies import initialize_dependencies
from .api.v1.endpoints import analysis, health, status
from .api.v1.dependencies import get_health_status


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application.
    """
    # Startup
    logging.info("Starting Tactics Master application...")
    
    # Initialize logging
    settings = get_settings()
    LoggingConfig.setup_logging(
        log_level=settings.get_log_level(),
        log_file=settings.logging.file_path,
        enable_structured=True,
        enable_performance=True
    )
    
    # Initialize dependencies
    initialize_dependencies()
    
    # Initialize agents
    try:
        from .core.dependencies import get_container
        container = get_container()
        
        # Initialize hybrid agent
        hybrid_agent = container.get("HybridTacticsMasterAgent")
        await hybrid_agent.initialize()
        logging.info("Hybrid agent initialized successfully")
        
    except Exception as e:
        logging.error(f"Failed to initialize agents: {e}")
        # Continue startup even if agents fail
    
    logging.info("Tactics Master application started successfully")
    
    yield
    
    # Shutdown
    logging.info("Shutting down Tactics Master application...")
    
    try:
        # Shutdown agents
        from .core.dependencies import get_container
        container = get_container()
        
        hybrid_agent = container.get("HybridTacticsMasterAgent")
        await hybrid_agent.shutdown()
        logging.info("Hybrid agent shutdown completed")
        
    except Exception as e:
        logging.error(f"Error during agent shutdown: {e}")
    
    logging.info("Tactics Master application shutdown completed")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    
    # Create FastAPI application
    app = FastAPI(
        title="Tactics Master API",
        version="2.0.0",
        description="""
        AI-powered cricket tactical analysis platform that provides intelligent
        insights for coaches, analysts, and cricket enthusiasts.
        
        ## Features
        
        * **Player Analysis**: Deep insights into individual player strengths, weaknesses, and tactical plans
        * **Team Analysis**: Comprehensive squad assessment with strategic recommendations
        * **Matchup Analysis**: Head-to-head records, venue factors, and historical trend analysis
        * **Tactical Planning**: Advanced bowling plans, fielding strategies, and execution recommendations
        
        ## Authentication
        
        Most endpoints require authentication. Use the `/auth/login` endpoint to obtain
        an access token, then include it in the Authorization header:
        
        ```
        Authorization: Bearer <your_access_token>
        ```
        
        ## Rate Limiting
        
        API requests are rate limited to prevent abuse. Current limits:
        - 100 requests per minute per user
        - 1000 requests per hour per user
        
        ## Error Handling
        
        The API uses standard HTTP status codes and returns detailed error information
        in the response body for debugging purposes.
        """,
        docs_url="/docs" if settings.is_development() else None,
        redoc_url="/redoc" if settings.is_development() else None,
        openapi_url="/openapi.json" if settings.is_development() else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware for production
    if settings.is_production():
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["tacticsmaster.com", "*.tacticsmaster.com"]
        )
    
    # Add custom middleware
    app = MiddlewareManager.setup_middleware(app)
    
    # Include API routers
    app.include_router(
        analysis.router,
        prefix="/api/v1",
        tags=["Analysis"]
    )
    
    app.include_router(
        health.router,
        prefix="/api/v1",
        tags=["Health"]
    )
    
    app.include_router(
        status.router,
        prefix="/api/v1",
        tags=["Status"]
    )
    
    # Add root endpoint
    @app.get("/", tags=["Root"])
    async def root() -> Dict[str, Any]:
        """
        Root endpoint providing basic API information.
        
        Returns:
            Dict containing API information
        """
        return {
            "message": "Tactics Master API",
            "version": "2.0.0",
            "status": "operational",
            "docs": "/docs" if settings.is_development() else "Contact support for API documentation",
            "health": "/api/v1/health"
        }
    
    # Add global exception handlers
    @app.exception_handler(TacticsMasterError)
    async def tactics_master_error_handler(request: Request, exc: TacticsMasterError) -> JSONResponse:
        """Handle TacticsMasterError exceptions"""
        error_response = ErrorHandler.format_error_response(exc)
        return JSONResponse(
            status_code=error_response.get("status_code", 500),
            content={
                "error": True,
                **error_response
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "error_code": "HTTP_ERROR",
                "message": exc.detail,
                "user_message": "An error occurred while processing your request",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle request validation errors"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(x) for x in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "user_message": "Please check your input parameters",
                "details": {
                    "validation_errors": errors
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions"""
        logging.critical(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "error_code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "user_message": "Something went wrong. Please try again later.",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        )
    
    return app


# Create application instance
app = create_application()


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Dict containing health status
    """
    try:
        health_status = await get_health_status()
        return health_status
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-01T12:00:00Z"
        }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logging.info("Tactics Master API started")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logging.info("Tactics Master API shutting down")


# Development server
if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development(),
        log_level=settings.get_log_level().lower(),
        access_log=True
    )
