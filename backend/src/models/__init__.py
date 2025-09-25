"""
Models package for Tactics Master Backend

This package contains Pydantic models for request/response validation,
data schemas, and type definitions.
"""

from .requests import (
    QueryRequest,
    BatchAnalysisRequest,
    HealthCheckRequest,
    ConfigurationRequest,
    FeedbackRequest,
    SearchRequest,
    MatchType,
    AnalysisType
)

from .responses import (
    QueryResponse,
    BatchAnalysisResponse,
    HealthResponse,
    ErrorResponse,
    SuccessResponse,
    SearchResponse,
    ConfigurationResponse,
    FeedbackResponse,
    AnalysisStatus,
    ResponseStatus
)

__all__ = [
    # Request models
    "QueryRequest",
    "BatchAnalysisRequest", 
    "HealthCheckRequest",
    "ConfigurationRequest",
    "FeedbackRequest",
    "SearchRequest",
    "MatchType",
    "AnalysisType",
    # Response models
    "QueryResponse",
    "BatchAnalysisResponse",
    "HealthResponse", 
    "ErrorResponse",
    "SuccessResponse",
    "SearchResponse",
    "ConfigurationResponse",
    "FeedbackResponse",
    "AnalysisStatus",
    "ResponseStatus"
]
