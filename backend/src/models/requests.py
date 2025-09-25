"""
Request models for Tactics Master API

This module defines Pydantic models for API request validation,
providing type safety and automatic validation for incoming requests.
"""

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum


class MatchType(str, Enum):
    """Enumeration of supported match types."""
    ODI = "ODI"
    T20 = "T20"
    TEST = "Test"
    T10 = "T10"


class AnalysisType(str, Enum):
    """Enumeration of supported analysis types."""
    PLAYER = "player"
    TEAM = "team"
    MATCHUP = "matchup"
    VENUE = "venue"
    GENERAL = "general"


class QueryRequest(BaseModel):
    """
    Request model for cricket analysis queries.
    
    This model validates incoming analysis requests and ensures
    proper data structure and content validation.
    """
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The cricket analysis query",
        example="Analyze Virat Kohli's weaknesses and create a bowling plan"
    )
    
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context for the analysis",
        example={
            "team": "India",
            "opponent": "Australia", 
            "venue": "Narendra Modi Stadium",
            "matchType": "ODI"
        }
    )
    
    analysis_type: Optional[AnalysisType] = Field(
        default=None,
        description="Type of analysis to perform"
    )
    
    priority: Optional[str] = Field(
        default="normal",
        description="Analysis priority level",
        regex="^(low|normal|high|urgent)$"
    )
    
    timeout: Optional[int] = Field(
        default=300,
        ge=30,
        le=600,
        description="Analysis timeout in seconds"
    )
    
    @validator("query")
    def validate_query(cls, v):
        """Validate query content."""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        
        # Check for potentially harmful content
        harmful_patterns = ["<script", "javascript:", "data:", "vbscript:"]
        query_lower = v.lower()
        for pattern in harmful_patterns:
            if pattern in query_lower:
                raise ValueError("Query contains potentially harmful content")
        
        return v.strip()
    
    @validator("context")
    def validate_context(cls, v):
        """Validate context structure."""
        if v is None:
            return {}
        
        # Check for reasonable context size
        if len(str(v)) > 10000:  # 10KB limit for context
            raise ValueError("Context is too large")
        
        return v
    
    @root_validator
    def validate_request(cls, values):
        """Validate the entire request."""
        query = values.get("query", "")
        context = values.get("context", {})
        
        # Check if query and context are compatible
        if context and "team" in context:
            # If team is specified, ensure query is relevant
            if not any(keyword in query.lower() for keyword in ["team", "squad", "lineup", "players"]):
                # This is just a warning, not an error
                pass
        
        return values
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "query": "Analyze Virat Kohli's weaknesses and create a bowling plan",
                "context": {
                    "team": "India",
                    "opponent": "Australia",
                    "venue": "Narendra Modi Stadium",
                    "matchType": "ODI"
                },
                "analysis_type": "player",
                "priority": "normal",
                "timeout": 300
            }
        }


class BatchAnalysisRequest(BaseModel):
    """
    Request model for batch analysis operations.
    
    This model supports analyzing multiple queries in a single request
    for improved efficiency and reduced API calls.
    """
    
    queries: List[QueryRequest] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of analysis queries"
    )
    
    batch_id: Optional[str] = Field(
        default=None,
        description="Optional batch identifier for tracking"
    )
    
    parallel: bool = Field(
        default=True,
        description="Whether to process queries in parallel"
    )
    
    @validator("queries")
    def validate_queries(cls, v):
        """Validate batch queries."""
        if not v:
            raise ValueError("At least one query is required")
        
        # Check for duplicate queries
        query_texts = [q.query for q in v]
        if len(query_texts) != len(set(query_texts)):
            raise ValueError("Duplicate queries are not allowed in batch requests")
        
        return v


class HealthCheckRequest(BaseModel):
    """
    Request model for health check operations.
    
    This model supports detailed health checks with specific
    component testing and diagnostics.
    """
    
    include_components: Optional[List[str]] = Field(
        default=None,
        description="Specific components to check"
    )
    
    detailed: bool = Field(
        default=False,
        description="Whether to include detailed diagnostics"
    )
    
    timeout: Optional[int] = Field(
        default=30,
        ge=5,
        le=120,
        description="Health check timeout in seconds"
    )


class ConfigurationRequest(BaseModel):
    """
    Request model for configuration updates.
    
    This model allows runtime configuration updates for
    system parameters and settings.
    """
    
    settings: Dict[str, Any] = Field(
        ...,
        description="Configuration settings to update"
    )
    
    validate_only: bool = Field(
        default=False,
        description="Whether to only validate without applying changes"
    )
    
    @validator("settings")
    def validate_settings(cls, v):
        """Validate configuration settings."""
        if not v:
            raise ValueError("Settings cannot be empty")
        
        # Check for reasonable settings size
        if len(str(v)) > 50000:  # 50KB limit for settings
            raise ValueError("Settings payload is too large")
        
        return v


class FeedbackRequest(BaseModel):
    """
    Request model for user feedback.
    
    This model captures user feedback on analysis results
    for continuous improvement and quality monitoring.
    """
    
    analysis_id: str = Field(
        ...,
        description="ID of the analysis to provide feedback for"
    )
    
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating from 1 (poor) to 5 (excellent)"
    )
    
    feedback: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional detailed feedback"
    )
    
    categories: Optional[List[str]] = Field(
        default=None,
        description="Feedback categories (accuracy, relevance, etc.)"
    )
    
    @validator("feedback")
    def validate_feedback(cls, v):
        """Validate feedback content."""
        if v and len(v.strip()) < 10:
            raise ValueError("Feedback must be at least 10 characters if provided")
        return v


class SearchRequest(BaseModel):
    """
    Request model for searching analysis history.
    
    This model supports searching through previous analyses
    with various filters and sorting options.
    """
    
    query: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Search query text"
    )
    
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Search filters"
    )
    
    sort_by: Optional[str] = Field(
        default="created_at",
        description="Field to sort by"
    )
    
    sort_order: Optional[str] = Field(
        default="desc",
        regex="^(asc|desc)$",
        description="Sort order"
    )
    
    limit: Optional[int] = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results"
    )
    
    offset: Optional[int] = Field(
        default=0,
        ge=0,
        description="Number of results to skip"
    )
