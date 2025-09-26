"""
Status API Endpoints for Tactics Master

This module provides status endpoints for monitoring agent status,
service availability, and system performance.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
from typing import Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies import get_hybrid_agent
from ...models.responses import StatusResponse, ErrorResponse

# Configure logging
logger = logging.getLogger("backend.api.status")

# Create router
router = APIRouter(
    prefix="/status",
    tags=["Status"],
    responses={
        200: {"model": StatusResponse, "description": "Status retrieved successfully"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    }
)


@router.get(
    "/",
    response_model=StatusResponse,
    summary="Get analysis service status",
    description="""
    Get the current status of the analysis service and agents.
    
    This endpoint provides detailed information about:
    - Service status (healthy, degraded, unhealthy)
    - Agent status and capabilities
    - Active requests and error counts
    - Performance metrics
    """,
    responses={
        200: {
            "description": "Status retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "service": "analysis",
                        "status": "healthy",
                        "agent": {
                            "name": "HybridTacticsMaster",
                            "status": "ready",
                            "active_requests": 0,
                            "error_count": 0,
                            "uptime_seconds": 86400.0
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        },
        503: {
            "description": "Service unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "service": "analysis",
                        "status": "unhealthy",
                        "agent": {
                            "name": "HybridTacticsMaster",
                            "status": "error",
                            "active_requests": 0,
                            "error_count": 5
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        }
    }
)
async def get_analysis_status() -> StatusResponse:
    """
    Get analysis service status.
    
    Returns:
        StatusResponse: Detailed status information
        
    Raises:
        HTTPException: If service is unavailable (503)
    """
    try:
        # Get hybrid agent
        hybrid_agent = get_hybrid_agent()
        
        if not hybrid_agent:
            raise HTTPException(
                status_code=503,
                detail="Hybrid agent not available"
            )
        
        # Get agent health status
        agent_health = await hybrid_agent.health_check()
        
        # Determine service status
        service_status = "healthy"
        if not agent_health.get("healthy", False):
            service_status = "degraded"
        
        # Get agent status info
        agent_info = hybrid_agent.get_status_info()
        
        # Create response
        response = StatusResponse(
            service="analysis",
            status=service_status,
            agent={
                "name": agent_info.get("name", "Unknown"),
                "status": agent_info.get("status", "unknown"),
                "active_requests": agent_info.get("active_requests", 0),
                "error_count": agent_info.get("error_count", 0),
                "uptime_seconds": agent_info.get("uptime_seconds", 0),
                "capabilities": agent_info.get("capabilities", [])
            },
            timestamp=datetime.now()
        )
        
        # Return appropriate status code
        if service_status == "unhealthy":
            return JSONResponse(
                status_code=503,
                content=response.dict()
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Status check failed: {str(e)}"
        )


@router.get(
    "/agent",
    summary="Get agent status",
    description="""
    Get detailed status information for the hybrid agent.
    
    This endpoint provides comprehensive agent information including:
    - Agent name and version
    - Current status and capabilities
    - Active requests and error counts
    - Performance metrics
    - Uptime and last activity
    """,
    responses={
        200: {
            "description": "Agent status retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "name": "HybridTacticsMaster",
                        "version": "2.0.0",
                        "status": "ready",
                        "capabilities": [
                            "data_analysis",
                            "tactical_planning",
                            "player_analysis",
                            "team_analysis"
                        ],
                        "active_requests": 0,
                        "max_concurrent_requests": 20,
                        "error_count": 0,
                        "uptime_seconds": 86400.0,
                        "last_activity": "2024-01-01T12:00:00Z",
                        "initialization_time": "2024-01-01T00:00:00Z"
                    }
                }
            }
        }
    }
)
async def get_agent_status() -> Dict[str, Any]:
    """
    Get detailed agent status.
    
    Returns:
        Dict containing detailed agent status information
    """
    try:
        # Get hybrid agent
        hybrid_agent = get_hybrid_agent()
        
        if not hybrid_agent:
            raise HTTPException(
                status_code=503,
                detail="Hybrid agent not available"
            )
        
        # Get comprehensive agent status
        agent_info = hybrid_agent.get_status_info()
        
        return agent_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent status check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Agent status check failed: {str(e)}"
        )


@router.get(
    "/capabilities",
    summary="Get agent capabilities",
    description="""
    Get the capabilities and features available from the hybrid agent.
    
    This endpoint provides information about:
    - Available analysis types
    - Supported data sources
    - Analysis capabilities
    - Tool availability
    """,
    responses={
        200: {
            "description": "Capabilities retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "agent_name": "HybridTacticsMaster",
                        "version": "2.0.0",
                        "capabilities": [
                            "data_analysis",
                            "tactical_planning",
                            "player_analysis",
                            "team_analysis",
                            "matchup_analysis",
                            "venue_analysis"
                        ],
                        "analysis_types": [
                            "comprehensive",
                            "player",
                            "team",
                            "matchup",
                            "venue",
                            "tactical"
                        ],
                        "data_sources": [
                            "CricAPI",
                            "ESPN Cricket",
                            "Historical Database"
                        ],
                        "tools": [
                            "get_player_stats",
                            "get_team_squad",
                            "get_matchup_data",
                            "get_venue_stats",
                            "analyze_weaknesses",
                            "find_best_matchup",
                            "generate_bowling_plan",
                            "generate_fielding_plan"
                        ]
                    }
                }
            }
        }
    }
)
async def get_capabilities() -> Dict[str, Any]:
    """
    Get agent capabilities and features.
    
    Returns:
        Dict containing agent capabilities information
    """
    try:
        # Get hybrid agent
        hybrid_agent = get_hybrid_agent()
        
        if not hybrid_agent:
            raise HTTPException(
                status_code=503,
                detail="Hybrid agent not available"
            )
        
        # Get agent capabilities
        capabilities = hybrid_agent.get_capabilities()
        
        # Get agent info
        agent_info = hybrid_agent.get_status_info()
        
        return {
            "agent_name": agent_info.get("name", "Unknown"),
            "version": agent_info.get("version", "Unknown"),
            "capabilities": [cap.value for cap in capabilities],
            "analysis_types": [
                "comprehensive",
                "player",
                "team",
                "matchup",
                "venue",
                "tactical"
            ],
            "data_sources": [
                "CricAPI",
                "ESPN Cricket",
                "Historical Database"
            ],
            "tools": [
                "get_player_stats",
                "get_team_squad",
                "get_matchup_data",
                "get_venue_stats",
                "analyze_weaknesses",
                "find_best_matchup",
                "generate_bowling_plan",
                "generate_fielding_plan"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Capabilities check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Capabilities check failed: {str(e)}"
        )


@router.get(
    "/performance",
    summary="Get performance metrics",
    description="""
    Get performance metrics for the analysis service.
    
    This endpoint provides detailed performance information including:
    - Request processing times
    - Success and error rates
    - Resource utilization
    - Agent performance metrics
    """,
    responses={
        200: {
            "description": "Performance metrics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2024-01-01T12:00:00Z",
                        "service_metrics": {
                            "total_requests": 1000,
                            "successful_requests": 950,
                            "failed_requests": 50,
                            "success_rate": 0.95,
                            "average_response_time": 1.23,
                            "p95_response_time": 2.50,
                            "p99_response_time": 4.20
                        },
                        "agent_metrics": {
                            "name": "HybridTacticsMaster",
                            "active_requests": 0,
                            "total_requests": 500,
                            "error_count": 5,
                            "uptime_seconds": 86400.0,
                            "average_processing_time": 1.15
                        },
                        "resource_metrics": {
                            "memory_usage_mb": 256.5,
                            "cpu_usage_percent": 15.2,
                            "disk_usage_percent": 45.8
                        }
                    }
                }
            }
        }
    }
)
async def get_performance_metrics() -> Dict[str, Any]:
    """
    Get performance metrics for the analysis service.
    
    Returns:
        Dict containing performance metrics
    """
    try:
        # Get hybrid agent
        hybrid_agent = get_hybrid_agent()
        
        if not hybrid_agent:
            raise HTTPException(
                status_code=503,
                detail="Hybrid agent not available"
            )
        
        # Get agent status info
        agent_info = hybrid_agent.get_status_info()
        
        # Calculate metrics
        total_requests = agent_info.get("total_requests", 0)
        error_count = agent_info.get("error_count", 0)
        successful_requests = max(0, total_requests - error_count)
        success_rate = successful_requests / total_requests if total_requests > 0 else 0
        
        # Get resource metrics (this would come from actual monitoring)
        resource_metrics = {
            "memory_usage_mb": 256.5,  # This would be actual memory usage
            "cpu_usage_percent": 15.2,  # This would be actual CPU usage
            "disk_usage_percent": 45.8  # This would be actual disk usage
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "service_metrics": {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": error_count,
                "success_rate": success_rate,
                "average_response_time": 1.23,  # This would be actual metrics
                "p95_response_time": 2.50,
                "p99_response_time": 4.20
            },
            "agent_metrics": {
                "name": agent_info.get("name", "Unknown"),
                "active_requests": agent_info.get("active_requests", 0),
                "total_requests": total_requests,
                "error_count": error_count,
                "uptime_seconds": agent_info.get("uptime_seconds", 0),
                "average_processing_time": 1.15  # This would be actual metrics
            },
            "resource_metrics": resource_metrics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Performance metrics check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Performance metrics check failed: {str(e)}"
        )
