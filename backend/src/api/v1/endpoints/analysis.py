"""
Analysis API Endpoints for Tactics Master

This module provides comprehensive API endpoints for cricket tactical analysis,
featuring robust error handling, input validation, and performance monitoring.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

from ...dependencies import (
    get_hybrid_agent,
    get_current_user,
    require_authentication,
    get_request_logger,
    get_performance_logger
)
from ...models.requests import AnalysisRequest, BatchAnalysisRequest
from ...models.responses import AnalysisResponse, BatchAnalysisResponse, ErrorResponse
from ...core.exceptions import (
    ValidationError,
    AgentExecutionError,
    ServiceUnavailableError
)
from ...core.validation import Validator
from ...core.logging import PerformanceLogger

# Configure logging
logger = logging.getLogger("backend.api.analysis")

# Create router
router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        429: {"model": ErrorResponse, "description": "Rate Limited"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"},
    }
)


class AnalysisRequest(BaseModel):
    """Request model for cricket analysis"""
    
    query: str = Field(
        ...,
        description="The cricket analysis query",
        min_length=1,
        max_length=2000,
        example="Analyze Virat Kohli's batting performance against spin bowling"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the analysis",
        example={"team": "India", "format": "ODI", "venue": "Wankhede Stadium"}
    )
    analysis_type: str = Field(
        default="comprehensive",
        description="Type of analysis to perform",
        regex="^(comprehensive|player|team|matchup|venue|tactical)$"
    )
    include_recommendations: bool = Field(
        default=True,
        description="Whether to include tactical recommendations"
    )
    include_statistics: bool = Field(
        default=True,
        description="Whether to include statistical analysis"
    )
    priority: str = Field(
        default="normal",
        description="Analysis priority level",
        regex="^(low|normal|high|urgent)$"
    )
    
    @validator('query')
    def validate_query(cls, v):
        """Validate analysis query"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=2000,
            field_name="query"
        )
    
    @validator('context')
    def validate_context(cls, v):
        """Validate analysis context"""
        if not isinstance(v, dict):
            raise ValueError("Context must be a dictionary")
        
        # Validate context size
        if len(str(v)) > 10000:  # 10KB limit
            raise ValueError("Context too large")
        
        return v


class AnalysisResponse(BaseModel):
    """Response model for cricket analysis"""
    
    success: bool = Field(..., description="Whether the analysis was successful")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    query: str = Field(..., description="Original analysis query")
    response: str = Field(..., description="Analysis response text")
    analysis: Dict[str, Any] = Field(..., description="Detailed analysis data")
    recommendations: List[str] = Field(default_factory=list, description="Tactical recommendations")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Statistical analysis")
    sources: List[str] = Field(default_factory=list, description="Data sources used")
    confidence: float = Field(..., description="Analysis confidence score", ge=0.0, le=1.0)
    processing_time: float = Field(..., description="Analysis processing time in seconds")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    agent_info: Dict[str, Any] = Field(..., description="Agent information")


class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis"""
    
    queries: List[AnalysisRequest] = Field(
        ...,
        description="List of analysis requests",
        min_items=1,
        max_items=10
    )
    batch_id: Optional[str] = Field(
        default=None,
        description="Optional batch identifier"
    )
    parallel: bool = Field(
        default=True,
        description="Whether to process queries in parallel"
    )


class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis"""
    
    success: bool = Field(..., description="Whether the batch analysis was successful")
    batch_id: str = Field(..., description="Batch identifier")
    results: List[AnalysisResponse] = Field(..., description="Analysis results")
    total_processing_time: float = Field(..., description="Total processing time in seconds")
    timestamp: datetime = Field(..., description="Batch analysis timestamp")


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Perform cricket tactical analysis",
    description="""
    Perform comprehensive cricket tactical analysis using AI agents.
    
    This endpoint analyzes cricket queries and provides:
    - Player performance analysis
    - Team tactical insights
    - Matchup analysis
    - Venue-specific recommendations
    - Tactical strategies and recommendations
    
    The analysis combines real cricket data with AI-powered insights to provide
    actionable recommendations for coaches and analysts.
    """,
    responses={
        200: {
            "description": "Analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "analysis_id": "analysis_123456",
                        "query": "Analyze Virat Kohli's batting performance",
                        "response": "Based on recent data, Virat Kohli shows...",
                        "analysis": {
                            "player_name": "Virat Kohli",
                            "recent_form": "Excellent",
                            "strengths": ["Against pace", "Death overs"],
                            "weaknesses": ["Against spin", "Early innings"]
                        },
                        "recommendations": [
                            "Use spin bowling early in innings",
                            "Set attacking fields for new batsman"
                        ],
                        "statistics": {
                            "batting_average": 52.3,
                            "strike_rate": 125.6
                        },
                        "sources": ["CricAPI", "ESPN Cricket"],
                        "confidence": 0.92,
                        "processing_time": 1.23,
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        }
    }
)
async def analyze_tactics(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(require_authentication),
    hybrid_agent = Depends(get_hybrid_agent),
    request_logger: logging.Logger = Depends(get_request_logger),
    performance_logger: PerformanceLogger = Depends(get_performance_logger)
) -> AnalysisResponse:
    """
    Perform cricket tactical analysis.
    
    Args:
        request: Analysis request with query and context
        background_tasks: FastAPI background tasks
        current_user: Authenticated user information
        hybrid_agent: Hybrid tactics master agent
        request_logger: Request logger instance
        performance_logger: Performance logger instance
        
    Returns:
        AnalysisResponse: Comprehensive analysis results
        
    Raises:
        HTTPException: If analysis fails or validation errors occur
    """
    import uuid
    import time
    
    analysis_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Log request
        request_logger.info(f"Analysis request received: {analysis_id}")
        performance_logger.start_timer(f"analysis_{analysis_id}")
        
        # Validate request
        validated_query = Validator.validate_string(
            value=request.query,
            required=True,
            min_length=1,
            max_length=2000,
            field_name="query"
        )
        
        validated_context = Validator.validate_json(
            value=request.context,
            required=False,
            field_name="context"
        )
        
        # Perform analysis
        analysis_result = await hybrid_agent.analyze(
            query=validated_query,
            context=validated_context
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        performance_logger.end_timer(f"analysis_{analysis_id}")
        
        # Extract analysis components
        response_text = analysis_result.get("response", "")
        analysis_data = analysis_result.get("analysis", {})
        sources = analysis_result.get("sources", [])
        
        # Generate recommendations if requested
        recommendations = []
        if request.include_recommendations:
            recommendations = _extract_recommendations(analysis_data)
        
        # Extract statistics if requested
        statistics = {}
        if request.include_statistics:
            statistics = _extract_statistics(analysis_data)
        
        # Calculate confidence score
        confidence = _calculate_confidence(analysis_data, sources)
        
        # Log successful analysis
        request_logger.info(f"Analysis completed successfully: {analysis_id}")
        
        # Schedule background tasks
        background_tasks.add_task(
            _log_analysis_metrics,
            analysis_id,
            processing_time,
            confidence,
            current_user.get("user_id")
        )
        
        return AnalysisResponse(
            success=True,
            analysis_id=analysis_id,
            query=validated_query,
            response=response_text,
            analysis=analysis_data,
            recommendations=recommendations,
            statistics=statistics,
            sources=sources,
            confidence=confidence,
            processing_time=processing_time,
            timestamp=datetime.now(),
            agent_info={
                "name": hybrid_agent.name,
                "version": hybrid_agent.version,
                "capabilities": [cap.value for cap in hybrid_agent.capabilities]
            }
        )
        
    except ValidationError as e:
        logger.error(f"Validation error in analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e.message}"
        )
    
    except AgentExecutionError as e:
        logger.error(f"Agent execution error in analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis execution failed: {e.message}"
        )
    
    except ServiceUnavailableError as e:
        logger.error(f"Service unavailable for analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Analysis service unavailable: {e.message}"
        )
    
    except Exception as e:
        logger.critical(f"Unexpected error in analysis {analysis_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis"
        )


@router.post(
    "/analyze/batch",
    response_model=BatchAnalysisResponse,
    summary="Perform batch cricket analysis",
    description="""
    Perform batch cricket tactical analysis for multiple queries.
    
    This endpoint allows processing multiple analysis queries in a single request,
    supporting both sequential and parallel processing modes.
    """,
    responses={
        200: {
            "description": "Batch analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "batch_id": "batch_123456",
                        "results": [
                            {
                                "success": True,
                                "analysis_id": "analysis_1",
                                "query": "Analyze player performance",
                                "response": "Analysis result...",
                                "confidence": 0.92
                            }
                        ],
                        "total_processing_time": 2.45,
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        }
    }
)
async def analyze_tactics_batch(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(require_authentication),
    hybrid_agent = Depends(get_hybrid_agent),
    request_logger: logging.Logger = Depends(get_request_logger)
) -> BatchAnalysisResponse:
    """
    Perform batch cricket tactical analysis.
    
    Args:
        request: Batch analysis request with multiple queries
        background_tasks: FastAPI background tasks
        current_user: Authenticated user information
        hybrid_agent: Hybrid tactics master agent
        request_logger: Request logger instance
        
    Returns:
        BatchAnalysisResponse: Batch analysis results
        
    Raises:
        HTTPException: If batch analysis fails
    """
    import uuid
    import time
    import asyncio
    
    batch_id = request.batch_id or str(uuid.uuid4())
    start_time = time.time()
    
    try:
        request_logger.info(f"Batch analysis request received: {batch_id}")
        
        # Validate batch request
        if len(request.queries) > 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Maximum 10 queries allowed per batch"
            )
        
        # Process queries
        if request.parallel:
            # Parallel processing
            tasks = [
                _process_single_analysis(query, hybrid_agent, request_logger)
                for query in request.queries
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Sequential processing
            results = []
            for query in request.queries:
                result = await _process_single_analysis(query, hybrid_agent, request_logger)
                results.append(result)
        
        # Calculate total processing time
        total_processing_time = time.time() - start_time
        
        # Log batch completion
        request_logger.info(f"Batch analysis completed: {batch_id}")
        
        # Schedule background tasks
        background_tasks.add_task(
            _log_batch_metrics,
            batch_id,
            total_processing_time,
            len(results),
            current_user.get("user_id")
        )
        
        return BatchAnalysisResponse(
            success=True,
            batch_id=batch_id,
            results=results,
            total_processing_time=total_processing_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Batch analysis error {batch_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch analysis failed"
        )


@router.get(
    "/status",
    summary="Get analysis service status",
    description="Get the current status of the analysis service and agents"
)
async def get_analysis_status(
    hybrid_agent = Depends(get_hybrid_agent)
) -> Dict[str, Any]:
    """
    Get analysis service status.
    
    Returns:
        Dict containing service status information
    """
    try:
        # Get agent health status
        agent_health = await hybrid_agent.health_check()
        
        return {
            "service": "analysis",
            "status": "healthy" if agent_health.get("healthy") else "degraded",
            "agent": agent_health,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "service": "analysis",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# Helper functions

def _extract_recommendations(analysis_data: Dict[str, Any]) -> List[str]:
    """Extract tactical recommendations from analysis data"""
    recommendations = []
    
    # Extract from various analysis sections
    if "recommendations" in analysis_data:
        recommendations.extend(analysis_data["recommendations"])
    
    if "tactical_opportunities" in analysis_data:
        recommendations.extend(analysis_data["tactical_opportunities"])
    
    if "key_recommendations" in analysis_data:
        recommendations.extend(analysis_data["key_recommendations"])
    
    return recommendations


def _extract_statistics(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract statistical data from analysis"""
    statistics = {}
    
    # Extract statistical information
    if "recent_form" in analysis_data:
        statistics["recent_form"] = analysis_data["recent_form"]
    
    if "career_stats" in analysis_data:
        statistics["career_stats"] = analysis_data["career_stats"]
    
    if "performance_metrics" in analysis_data:
        statistics["performance_metrics"] = analysis_data["performance_metrics"]
    
    return statistics


def _calculate_confidence(analysis_data: Dict[str, Any], sources: List[str]) -> float:
    """Calculate analysis confidence score"""
    confidence = 0.5  # Base confidence
    
    # Increase confidence based on data sources
    if sources:
        confidence += 0.2
    
    # Increase confidence based on analysis depth
    if "detailed_analysis" in analysis_data:
        confidence += 0.1
    
    if "statistical_analysis" in analysis_data:
        confidence += 0.1
    
    if "tactical_recommendations" in analysis_data:
        confidence += 0.1
    
    return min(confidence, 1.0)


async def _process_single_analysis(
    query: AnalysisRequest,
    hybrid_agent,
    request_logger: logging.Logger
) -> AnalysisResponse:
    """Process a single analysis query"""
    import uuid
    import time
    
    analysis_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Perform analysis
        result = await hybrid_agent.analyze(
            query=query.query,
            context=query.context
        )
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            success=True,
            analysis_id=analysis_id,
            query=query.query,
            response=result.get("response", ""),
            analysis=result.get("analysis", {}),
            recommendations=_extract_recommendations(result.get("analysis", {})),
            statistics=_extract_statistics(result.get("analysis", {})),
            sources=result.get("sources", []),
            confidence=_calculate_confidence(result.get("analysis", {}), result.get("sources", [])),
            processing_time=processing_time,
            timestamp=datetime.now(),
            agent_info={
                "name": hybrid_agent.name,
                "version": hybrid_agent.version
            }
        )
        
    except Exception as e:
        request_logger.error(f"Single analysis failed {analysis_id}: {e}")
        return AnalysisResponse(
            success=False,
            analysis_id=analysis_id,
            query=query.query,
            response=f"Analysis failed: {str(e)}",
            analysis={},
            recommendations=[],
            statistics={},
            sources=[],
            confidence=0.0,
            processing_time=time.time() - start_time,
            timestamp=datetime.now(),
            agent_info={}
        )


async def _log_analysis_metrics(
    analysis_id: str,
    processing_time: float,
    confidence: float,
    user_id: Optional[str]
) -> None:
    """Log analysis metrics for monitoring"""
    logger.info(f"Analysis metrics: {analysis_id}, time: {processing_time:.3f}s, confidence: {confidence:.2f}, user: {user_id}")


async def _log_batch_metrics(
    batch_id: str,
    total_time: float,
    result_count: int,
    user_id: Optional[str]
) -> None:
    """Log batch analysis metrics for monitoring"""
    logger.info(f"Batch metrics: {batch_id}, time: {total_time:.3f}s, results: {result_count}, user: {user_id}")
