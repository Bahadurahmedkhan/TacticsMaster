"""
Response models for Tactics Master API

This module defines Pydantic models for API response validation,
providing consistent response structure and type safety.
"""

from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class AnalysisStatus(str, Enum):
    """Enumeration of analysis statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class ResponseStatus(str, Enum):
    """Enumeration of response statuses."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class QueryResponse(BaseModel):
    """
    Response model for cricket analysis results.
    
    This model provides a structured response format for analysis
    results with metadata and source information.
    """
    
    response: str = Field(
        ...,
        description="The analysis response text",
        example="# 🏏 Tactical Analysis: Virat Kohli\n\n## 📊 Overall Assessment..."
    )
    
    analysis: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Raw analysis data and metadata"
    )
    
    sources: List[str] = Field(
        default_factory=list,
        description="Data sources used in the analysis"
    )
    
    analysis_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this analysis"
    )
    
    status: AnalysisStatus = Field(
        default=AnalysisStatus.COMPLETED,
        description="Status of the analysis"
    )
    
    execution_time: Optional[float] = Field(
        default=None,
        description="Analysis execution time in seconds"
    )
    
    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score for the analysis (0-1)"
    )
    
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when analysis was created"
    )
    
    @validator("sources")
    def validate_sources(cls, v):
        """Validate sources list."""
        if not isinstance(v, list):
            raise ValueError("Sources must be a list")
        
        # Ensure all sources are strings
        for source in v:
            if not isinstance(source, str):
                raise ValueError("All sources must be strings")
        
        return v
    
    @validator("confidence_score")
    def validate_confidence_score(cls, v):
        """Validate confidence score."""
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "response": "# 🏏 Tactical Analysis: Virat Kohli\n\n## 📊 Overall Assessment\nVirat Kohli is in excellent form...",
                "analysis": {
                    "player_name": "Virat Kohli",
                    "weaknesses": ["against_spin", "early_innings"],
                    "strengths": ["death_overs", "against_pace"]
                },
                "sources": ["CricAPI", "Historical Data", "AI Analysis"],
                "analysis_id": "analysis_123456",
                "status": "completed",
                "execution_time": 2.5,
                "confidence_score": 0.85,
                "created_at": "2024-01-01T12:00:00Z"
            }
        }


class BatchAnalysisResponse(BaseModel):
    """
    Response model for batch analysis operations.
    
    This model provides results for multiple analysis queries
    in a single response with batch-level metadata.
    """
    
    results: List[QueryResponse] = Field(
        ...,
        description="List of analysis results"
    )
    
    batch_id: Optional[str] = Field(
        default=None,
        description="Batch identifier"
    )
    
    total_queries: int = Field(
        ...,
        description="Total number of queries in the batch"
    )
    
    successful_queries: int = Field(
        ...,
        description="Number of successfully processed queries"
    )
    
    failed_queries: int = Field(
        ...,
        description="Number of failed queries"
    )
    
    total_execution_time: Optional[float] = Field(
        default=None,
        description="Total execution time for the batch"
    )
    
    @validator("results")
    def validate_results(cls, v):
        """Validate results list."""
        if not isinstance(v, list):
            raise ValueError("Results must be a list")
        return v
    
    @validator("successful_queries", "failed_queries")
    def validate_query_counts(cls, v, values):
        """Validate query counts."""
        total = values.get("total_queries", 0)
        if v > total:
            raise ValueError("Query counts cannot exceed total queries")
        return v


class HealthResponse(BaseModel):
    """
    Response model for health check operations.
    
    This model provides comprehensive health status information
    including component status and system metrics.
    """
    
    status: str = Field(
        ...,
        description="Overall health status",
        example="healthy"
    )
    
    agent_available: bool = Field(
        ...,
        description="Whether the analysis agent is available"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Health check timestamp"
    )
    
    version: str = Field(
        ...,
        description="Application version"
    )
    
    uptime: Optional[float] = Field(
        default=None,
        description="Application uptime in seconds"
    )
    
    components: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Individual component health status"
    )
    
    metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="System metrics and performance data"
    )
    
    @validator("status")
    def validate_status(cls, v):
        """Validate health status."""
        allowed_statuses = ["healthy", "degraded", "unhealthy", "maintenance"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v


class ErrorResponse(BaseModel):
    """
    Response model for error conditions.
    
    This model provides structured error information with
    error codes, context, and debugging information.
    """
    
    error: str = Field(
        ...,
        description="Error message",
        example="Analysis failed due to invalid query"
    )
    
    error_code: Optional[str] = Field(
        default=None,
        description="Standardized error code",
        example="ANALYSIS_FAILED"
    )
    
    status_code: int = Field(
        ...,
        description="HTTP status code",
        example=500
    )
    
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )
    
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Error context information"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
    
    request_id: Optional[str] = Field(
        default=None,
        description="Request identifier for tracking"
    )
    
    retry_after: Optional[int] = Field(
        default=None,
        description="Seconds to wait before retrying (if applicable)"
    )


class SuccessResponse(BaseModel):
    """
    Response model for successful operations.
    
    This model provides a consistent format for successful
    operations with optional data payload.
    """
    
    status: ResponseStatus = Field(
        default=ResponseStatus.SUCCESS,
        description="Response status"
    )
    
    message: str = Field(
        ...,
        description="Success message",
        example="Analysis completed successfully"
    )
    
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Response data payload"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    request_id: Optional[str] = Field(
        default=None,
        description="Request identifier"
    )


class SearchResponse(BaseModel):
    """
    Response model for search operations.
    
    This model provides search results with pagination
    and metadata information.
    """
    
    results: List[Dict[str, Any]] = Field(
        ...,
        description="Search results"
    )
    
    total_count: int = Field(
        ...,
        description="Total number of matching results"
    )
    
    page: int = Field(
        ...,
        description="Current page number"
    )
    
    page_size: int = Field(
        ...,
        description="Number of results per page"
    )
    
    total_pages: int = Field(
        ...,
        description="Total number of pages"
    )
    
    has_next: bool = Field(
        ...,
        description="Whether there are more pages"
    )
    
    has_previous: bool = Field(
        ...,
        description="Whether there are previous pages"
    )


class ConfigurationResponse(BaseModel):
    """
    Response model for configuration operations.
    
    This model provides configuration information and
    validation results.
    """
    
    settings: Dict[str, Any] = Field(
        ...,
        description="Configuration settings"
    )
    
    valid: bool = Field(
        ...,
        description="Whether configuration is valid"
    )
    
    errors: Optional[List[str]] = Field(
        default=None,
        description="Configuration validation errors"
    )
    
    warnings: Optional[List[str]] = Field(
        default=None,
        description="Configuration warnings"
    )
    
    applied: bool = Field(
        default=False,
        description="Whether configuration was applied"
    )


class FeedbackResponse(BaseModel):
    """
    Response model for feedback operations.
    
    This model confirms feedback submission and provides
    feedback processing information.
    """
    
    feedback_id: str = Field(
        ...,
        description="Unique feedback identifier"
    )
    
    received: bool = Field(
        ...,
        description="Whether feedback was received"
    )
    
    processed: bool = Field(
        default=False,
        description="Whether feedback was processed"
    )
    
    message: str = Field(
        ...,
        description="Confirmation message"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Feedback submission timestamp"
    )
