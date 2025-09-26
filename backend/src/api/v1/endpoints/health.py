"""
Health Check API Endpoints for Tactics Master

This module provides comprehensive health check endpoints for monitoring
service status, component health, and system metrics.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ...dependencies import get_health_status, get_hybrid_agent
from ...models.responses import HealthResponse, ErrorResponse

# Configure logging
logger = logging.getLogger("backend.api.health")

# Create router
router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={
        200: {"model": HealthResponse, "description": "Health check successful"},
        503: {"model": ErrorResponse, "description": "Service unhealthy"},
    }
)


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Get service health status",
    description="""
    Get comprehensive health status of the Tactics Master service.
    
    This endpoint provides detailed information about:
    - Overall service health
    - Component status (database, agents, APIs)
    - Service metrics and performance
    - Uptime and version information
    
    Returns 200 if healthy, 503 if unhealthy.
    """,
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "service": "tactics-master-api",
                        "version": "2.0.0",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "uptime": 86400.0,
                        "components": {
                            "database": "healthy",
                            "redis": "healthy",
                            "agents": "healthy",
                            "apis": "healthy"
                        },
                        "metrics": {
                            "total_requests": 1000,
                            "successful_requests": 950,
                            "failed_requests": 50,
                            "average_response_time": 1.23
                        }
                    }
                }
            }
        },
        503: {
            "description": "Service is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "service": "tactics-master-api",
                        "version": "2.0.0",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "uptime": 86400.0,
                        "components": {
                            "database": "healthy",
                            "redis": "unhealthy",
                            "agents": "degraded",
                            "apis": "healthy"
                        },
                        "metrics": {
                            "total_requests": 1000,
                            "successful_requests": 800,
                            "failed_requests": 200,
                            "average_response_time": 2.45
                        }
                    }
                }
            }
        }
    }
)
async def get_health() -> HealthResponse:
    """
    Get comprehensive service health status.
    
    Returns:
        HealthResponse: Detailed health status information
        
    Raises:
        HTTPException: If service is unhealthy (503)
    """
    try:
        # Get health status
        health_data = await get_health_status()
        
        # Determine overall status
        overall_status = "healthy"
        if health_data.get("status") == "degraded":
            overall_status = "degraded"
        elif health_data.get("status") == "unhealthy":
            overall_status = "unhealthy"
        
        # Check component health
        components = health_data.get("services", {})
        unhealthy_components = [
            name for name, status in components.items() 
            if status not in ["healthy", "available"]
        ]
        
        if unhealthy_components:
            overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
        
        # Create response
        response = HealthResponse(
            status=overall_status,
            service="tactics-master-api",
            version="2.0.0",
            timestamp=datetime.now(),
            uptime=health_data.get("uptime", 0.0),
            components=components,
            metrics=health_data.get("metrics", {})
        )
        
        # Return appropriate status code
        if overall_status == "unhealthy":
            return JSONResponse(
                status_code=503,
                content=response.dict()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        
        # Return unhealthy status
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "tactics-master-api",
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat(),
                "uptime": 0.0,
                "components": {},
                "metrics": {},
                "error": str(e)
            }
        )


@router.get(
    "/liveness",
    summary="Liveness probe",
    description="""
    Simple liveness probe for Kubernetes and container orchestration.
    
    Returns 200 if the service is alive and responding to requests.
    This endpoint is designed to be lightweight and fast.
    """,
    responses={
        200: {"description": "Service is alive"},
        503: {"description": "Service is not responding"}
    }
)
async def liveness_probe() -> Dict[str, Any]:
    """
    Liveness probe endpoint.
    
    Returns:
        Dict containing liveness status
    """
    try:
        return {
            "status": "alive",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Liveness probe failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service is not responding"
        )


@router.get(
    "/readiness",
    summary="Readiness probe",
    description="""
    Readiness probe for Kubernetes and container orchestration.
    
    Returns 200 if the service is ready to handle requests.
    This endpoint checks if all required components are available.
    """,
    responses={
        200: {"description": "Service is ready"},
        503: {"description": "Service is not ready"}
    }
)
async def readiness_probe() -> Dict[str, Any]:
    """
    Readiness probe endpoint.
    
    Returns:
        Dict containing readiness status
    """
    try:
        # Check if agents are ready
        hybrid_agent = get_hybrid_agent()
        if not hybrid_agent or not hybrid_agent.is_ready:
            raise HTTPException(
                status_code=503,
                detail="Agents are not ready"
            )
        
        return {
            "status": "ready",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness probe failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service is not ready"
        )


@router.get(
    "/metrics",
    summary="Get service metrics",
    description="""
    Get detailed service metrics and performance data.
    
    This endpoint provides comprehensive metrics including:
    - Request counts and rates
    - Response times and percentiles
    - Error rates and types
    - Resource utilization
    - Agent performance metrics
    """,
    responses={
        200: {
            "description": "Metrics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "requests": {
                            "total": 1000,
                            "successful": 950,
                            "failed": 50,
                            "rate_per_minute": 10.5
                        },
                        "response_times": {
                            "average": 1.23,
                            "p50": 1.10,
                            "p95": 2.50,
                            "p99": 4.20
                        },
                        "errors": {
                            "total": 50,
                            "by_type": {
                                "validation_error": 20,
                                "agent_error": 15,
                                "timeout": 10,
                                "other": 5
                            }
                        },
                        "agents": {
                            "hybrid_agent": {
                                "status": "ready",
                                "active_requests": 0,
                                "total_requests": 500,
                                "error_count": 5
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_metrics() -> Dict[str, Any]:
    """
    Get detailed service metrics.
    
    Returns:
        Dict containing service metrics
    """
    try:
        # Get basic metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "requests": {
                "total": 1000,  # This would come from actual metrics
                "successful": 950,
                "failed": 50,
                "rate_per_minute": 10.5
            },
            "response_times": {
                "average": 1.23,
                "p50": 1.10,
                "p95": 2.50,
                "p99": 4.20
            },
            "errors": {
                "total": 50,
                "by_type": {
                    "validation_error": 20,
                    "agent_error": 15,
                    "timeout": 10,
                    "other": 5
                }
            }
        }
        
        # Get agent metrics
        try:
            hybrid_agent = get_hybrid_agent()
            if hybrid_agent:
                agent_info = hybrid_agent.get_status_info()
                metrics["agents"] = {
                    "hybrid_agent": {
                        "status": agent_info.get("status"),
                        "active_requests": agent_info.get("active_requests", 0),
                        "error_count": agent_info.get("error_count", 0),
                        "uptime_seconds": agent_info.get("uptime_seconds", 0)
                    }
                }
        except Exception as e:
            logger.warning(f"Failed to get agent metrics: {e}")
            metrics["agents"] = {"hybrid_agent": {"status": "unknown"}}
        
        return metrics
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve metrics"
        )


@router.get(
    "/version",
    summary="Get service version information",
    description="""
    Get detailed version information for the service and its components.
    
    This endpoint provides version information for:
    - Service version
    - Agent versions
    - Dependency versions
    - Build information
    """,
    responses={
        200: {
            "description": "Version information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "service": {
                            "name": "tactics-master-api",
                            "version": "2.0.0",
                            "build_date": "2024-01-01T00:00:00Z",
                            "git_commit": "abc123def456"
                        },
                        "agents": {
                            "hybrid_agent": {
                                "name": "HybridTacticsMaster",
                                "version": "2.0.0",
                                "capabilities": ["data_analysis", "tactical_planning"]
                            }
                        },
                        "dependencies": {
                            "fastapi": "0.104.0",
                            "langchain": "0.1.0",
                            "pydantic": "2.5.0"
                        }
                    }
                }
            }
        }
    }
)
async def get_version() -> Dict[str, Any]:
    """
    Get service version information.
    
    Returns:
        Dict containing version information
    """
    try:
        version_info = {
            "service": {
                "name": "tactics-master-api",
                "version": "2.0.0",
                "build_date": "2024-01-01T00:00:00Z",
                "git_commit": "abc123def456"  # This would come from build info
            },
            "agents": {},
            "dependencies": {
                "fastapi": "0.104.0",
                "langchain": "0.1.0",
                "pydantic": "2.5.0",
                "uvicorn": "0.24.0"
            }
        }
        
        # Get agent version information
        try:
            hybrid_agent = get_hybrid_agent()
            if hybrid_agent:
                agent_info = hybrid_agent.get_status_info()
                version_info["agents"]["hybrid_agent"] = {
                    "name": agent_info.get("name"),
                    "version": agent_info.get("version"),
                    "capabilities": agent_info.get("capabilities", [])
                }
        except Exception as e:
            logger.warning(f"Failed to get agent version info: {e}")
        
        return version_info
        
    except Exception as e:
        logger.error(f"Failed to get version info: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve version information"
        )
