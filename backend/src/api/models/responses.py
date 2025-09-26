"""
Response Models for Tactics Master API

This module defines comprehensive response models with validation,
documentation, and examples for all API endpoints.

Author: Tactics Master Team
Version: 2.0.0
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class AnalysisStatus(str, Enum):
    """Analysis status enumeration"""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"


class ConfidenceLevel(str, Enum):
    """Confidence level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AnalysisResponse(BaseModel):
    """
    Response model for cricket tactical analysis.
    
    This model defines the structure for analysis responses with comprehensive
    data and metadata.
    """
    
    success: bool = Field(
        ...,
        description="Whether the analysis was successful",
        example=True,
        title="Success Status"
    )
    
    analysis_id: str = Field(
        ...,
        description="Unique analysis identifier",
        min_length=1,
        max_length=100,
        example="analysis_123456789",
        title="Analysis ID"
    )
    
    query: str = Field(
        ...,
        description="Original analysis query",
        example="Analyze Virat Kohli's batting performance against spin bowling",
        title="Original Query"
    )
    
    response: str = Field(
        ...,
        description="Analysis response text",
        min_length=1,
        example="Based on recent data, Virat Kohli shows excellent form against pace bowling but struggles against quality spin...",
        title="Analysis Response"
    )
    
    analysis: Dict[str, Any] = Field(
        ...,
        description="Detailed analysis data",
        example={
            "player_name": "Virat Kohli",
            "recent_form": "Excellent",
            "strengths": ["Against pace", "Death overs", "Chase master"],
            "weaknesses": ["Against spin", "Early innings", "New ball"],
            "key_insights": [
                "Averages 45+ against pace in last 10 matches",
                "Strike rate drops to 85 against quality spin",
                "Most effective in middle overs (11-40)"
            ]
        },
        title="Detailed Analysis"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Tactical recommendations",
        example=[
            "Use spin bowling early in innings",
            "Set attacking fields for new batsman",
            "Target with short balls in middle overs"
        ],
        title="Tactical Recommendations"
    )
    
    statistics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Statistical analysis",
        example={
            "batting_average": 52.3,
            "strike_rate": 125.6,
            "recent_matches": 8,
            "runs_scored": 420,
            "centuries": 1,
            "fifties": 3
        },
        title="Statistical Data"
    )
    
    sources: List[str] = Field(
        default_factory=list,
        description="Data sources used",
        example=["CricAPI", "ESPN Cricket", "Historical Database"],
        title="Data Sources"
    )
    
    confidence: float = Field(
        ...,
        description="Analysis confidence score",
        ge=0.0,
        le=1.0,
        example=0.92,
        title="Confidence Score"
    )
    
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Confidence level category",
        example="high",
        title="Confidence Level"
    )
    
    processing_time: float = Field(
        ...,
        description="Analysis processing time in seconds",
        ge=0.0,
        example=1.23,
        title="Processing Time"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Analysis timestamp",
        example="2024-01-01T12:00:00Z",
        title="Analysis Timestamp"
    )
    
    agent_info: Dict[str, Any] = Field(
        ...,
        description="Agent information",
        example={
            "name": "HybridTacticsMaster",
            "version": "2.0.0",
            "capabilities": ["data_analysis", "tactical_planning", "player_analysis"]
        },
        title="Agent Information"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
        example={
            "analysis_type": "player",
            "language": "en",
            "priority": "normal",
            "user_id": "user_123"
        },
        title="Metadata"
    )
    
    @validator('confidence_level')
    def validate_confidence_level(cls, v, values):
        """Validate confidence level based on confidence score"""
        confidence = values.get('confidence', 0.0)
        
        if confidence >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 0.7:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "analysis_id": "analysis_123456789",
                "query": "Analyze Virat Kohli's batting performance against spin bowling",
                "response": "Based on recent data, Virat Kohli shows excellent form...",
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
                "confidence_level": "high",
                "processing_time": 1.23,
                "timestamp": "2024-01-01T12:00:00Z",
                "agent_info": {
                    "name": "HybridTacticsMaster",
                    "version": "2.0.0"
                }
            }
        }


class BatchAnalysisResponse(BaseModel):
    """
    Response model for batch cricket analysis.
    """
    
    success: bool = Field(
        ...,
        description="Whether the batch analysis was successful",
        example=True,
        title="Success Status"
    )
    
    batch_id: str = Field(
        ...,
        description="Batch identifier",
        min_length=1,
        max_length=100,
        example="batch_2024_001",
        title="Batch ID"
    )
    
    results: List[AnalysisResponse] = Field(
        ...,
        description="Analysis results",
        min_items=1,
        title="Analysis Results"
    )
    
    total_processing_time: float = Field(
        ...,
        description="Total batch processing time in seconds",
        ge=0.0,
        example=2.45,
        title="Total Processing Time"
    )
    
    successful_analyses: int = Field(
        ...,
        description="Number of successful analyses",
        ge=0,
        example=8,
        title="Successful Analyses"
    )
    
    failed_analyses: int = Field(
        ...,
        description="Number of failed analyses",
        ge=0,
        example=2,
        title="Failed Analyses"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Batch analysis timestamp",
        example="2024-01-01T12:00:00Z",
        title="Batch Timestamp"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Batch metadata",
        example={
            "parallel_processing": True,
            "total_queries": 10,
            "average_processing_time": 0.245
        },
        title="Batch Metadata"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "batch_id": "batch_2024_001",
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
                "successful_analyses": 8,
                "failed_analyses": 2,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Response model for API errors.
    """
    
    error: bool = Field(
        True,
        description="Error indicator",
        example=True,
        title="Error Status"
    )
    
    error_code: str = Field(
        ...,
        description="Error code",
        min_length=1,
        max_length=50,
        example="VALIDATION_ERROR",
        title="Error Code"
    )
    
    message: str = Field(
        ...,
        description="Error message",
        min_length=1,
        max_length=500,
        example="Invalid input parameters",
        title="Error Message"
    )
    
    user_message: str = Field(
        ...,
        description="User-friendly error message",
        min_length=1,
        max_length=500,
        example="Please check your input and try again",
        title="User Message"
    )
    
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details",
        example={
            "field": "query",
            "reason": "Query cannot be empty"
        },
        title="Error Details"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Error timestamp",
        example="2024-01-01T12:00:00Z",
        title="Error Timestamp"
    )
    
    request_id: Optional[str] = Field(
        default=None,
        description="Request identifier for tracking",
        example="req_123456789",
        title="Request ID"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": "Invalid input parameters",
                "user_message": "Please check your input and try again",
                "details": {
                    "field": "query",
                    "reason": "Query cannot be empty"
                },
                "timestamp": "2024-01-01T12:00:00Z",
                "request_id": "req_123456789"
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health checks.
    """
    
    status: str = Field(
        ...,
        description="Service health status",
        example="healthy",
        title="Health Status"
    )
    
    service: str = Field(
        ...,
        description="Service name",
        example="tactics-master-api",
        title="Service Name"
    )
    
    version: str = Field(
        ...,
        description="Service version",
        example="2.0.0",
        title="Service Version"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Health check timestamp",
        example="2024-01-01T12:00:00Z",
        title="Health Check Timestamp"
    )
    
    uptime: float = Field(
        ...,
        description="Service uptime in seconds",
        ge=0.0,
        example=86400.0,
        title="Service Uptime"
    )
    
    components: Dict[str, Any] = Field(
        ...,
        description="Component health status",
        example={
            "database": "healthy",
            "redis": "healthy",
            "agents": "healthy",
            "apis": "degraded"
        },
        title="Component Status"
    )
    
    metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Service metrics",
        example={
            "total_requests": 1000,
            "successful_requests": 950,
            "failed_requests": 50,
            "average_response_time": 1.23
        },
        title="Service Metrics"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "tactics-master-api",
                "version": "2.0.0",
                "timestamp": "2024-01-01T12:00:00Z",
                "uptime": 86400.0,
                "components": {
                    "database": "healthy",
                    "redis": "healthy",
                    "agents": "healthy"
                },
                "metrics": {
                    "total_requests": 1000,
                    "successful_requests": 950,
                    "average_response_time": 1.23
                }
            }
        }


class StatusResponse(BaseModel):
    """
    Response model for service status.
    """
    
    service: str = Field(
        ...,
        description="Service name",
        example="analysis",
        title="Service Name"
    )
    
    status: str = Field(
        ...,
        description="Service status",
        example="healthy",
        title="Service Status"
    )
    
    agent: Dict[str, Any] = Field(
        ...,
        description="Agent status information",
        example={
            "name": "HybridTacticsMaster",
            "status": "ready",
            "active_requests": 0,
            "error_count": 0
        },
        title="Agent Status"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Status check timestamp",
        example="2024-01-01T12:00:00Z",
        title="Status Timestamp"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "service": "analysis",
                "status": "healthy",
                "agent": {
                    "name": "HybridTacticsMaster",
                    "status": "ready",
                    "active_requests": 0,
                    "error_count": 0
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class PlayerAnalysisResponse(BaseModel):
    """
    Response model for player-specific analysis.
    """
    
    success: bool = Field(
        ...,
        description="Whether the analysis was successful",
        example=True,
        title="Success Status"
    )
    
    player_name: str = Field(
        ...,
        description="Player name",
        example="Virat Kohli",
        title="Player Name"
    )
    
    analysis_focus: str = Field(
        ...,
        description="Analysis focus area",
        example="batting",
        title="Analysis Focus"
    )
    
    time_period: str = Field(
        ...,
        description="Analysis time period",
        example="recent",
        title="Time Period"
    )
    
    format: str = Field(
        ...,
        description="Cricket format analyzed",
        example="odi",
        title="Cricket Format"
    )
    
    performance_summary: Dict[str, Any] = Field(
        ...,
        description="Performance summary",
        example={
            "matches_played": 15,
            "runs_scored": 750,
            "batting_average": 50.0,
            "strike_rate": 120.0,
            "centuries": 2,
            "fifties": 4
        },
        title="Performance Summary"
    )
    
    strengths: List[str] = Field(
        ...,
        description="Player strengths",
        example=["Against pace", "Death overs", "Chase master"],
        title="Player Strengths"
    )
    
    weaknesses: List[str] = Field(
        ...,
        description="Player weaknesses",
        example=["Against spin", "Early innings", "New ball"],
        title="Player Weaknesses"
    )
    
    recommendations: List[str] = Field(
        ...,
        description="Tactical recommendations",
        example=[
            "Use spin bowling early in innings",
            "Set attacking fields for new batsman"
        ],
        title="Tactical Recommendations"
    )
    
    confidence: float = Field(
        ...,
        description="Analysis confidence score",
        ge=0.0,
        le=1.0,
        example=0.92,
        title="Confidence Score"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Analysis timestamp",
        example="2024-01-01T12:00:00Z",
        title="Analysis Timestamp"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "player_name": "Virat Kohli",
                "analysis_focus": "batting",
                "time_period": "recent",
                "format": "odi",
                "performance_summary": {
                    "matches_played": 15,
                    "runs_scored": 750,
                    "batting_average": 50.0,
                    "strike_rate": 120.0
                },
                "strengths": ["Against pace", "Death overs"],
                "weaknesses": ["Against spin", "Early innings"],
                "recommendations": [
                    "Use spin bowling early in innings",
                    "Set attacking fields for new batsman"
                ],
                "confidence": 0.92,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
