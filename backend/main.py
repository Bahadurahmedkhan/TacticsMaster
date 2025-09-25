"""
Tactics Master Backend API

This module provides the FastAPI backend for the Tactics Master cricket analysis system.
It exposes REST endpoints for cricket tactical analysis using AI agents.

Author: Tactics Master Team
Version: 1.0.0
"""

import logging
from typing import List, Dict, Any, Optional
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from hybrid_agent import HybridTacticsMasterAgent

# Import custom exceptions
from exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ConfigurationError,
    ValidationError,
    ServiceUnavailableError
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tactics Master Agent API",
    version="1.0.0",
    description="AI-powered cricket tactical analysis API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the hybrid agent
try:
    agent = HybridTacticsMasterAgent()
    logger.info("Hybrid agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize hybrid agent: {e}")
    agent = None

class QueryRequest(BaseModel):
    """Request model for cricket analysis queries"""
    query: str = Field(..., description="The cricket analysis query", min_length=1, max_length=1000)
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for the analysis")

class QueryResponse(BaseModel):
    """Response model for cricket analysis results"""
    response: str = Field(..., description="The analysis response")
    analysis: Dict[str, Any] = Field(default_factory=dict, description="Raw analysis data")
    sources: List[str] = Field(default_factory=list, description="Data sources used")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Health status")
    agent_available: bool = Field(..., description="Whether the agent is available")
    timestamp: str = Field(..., description="Current timestamp")

@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """
    Root endpoint providing basic API information.
    
    Returns:
        Dict[str, str]: Basic API information
    """
    return {
        "message": "Tactics Master Agent API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/analyze", response_model=QueryResponse, tags=["Analysis"])
async def analyze_tactics(request: QueryRequest) -> QueryResponse:
    """
    Analyze cricket tactics based on coach query.
    
    This endpoint processes cricket analysis queries and returns tactical insights,
    player analysis, and strategic recommendations.
    
    Args:
        request: The analysis request containing query and context
        
    Returns:
        QueryResponse: Analysis results with response, analysis data, and sources
        
    Raises:
        HTTPException: If analysis fails or agent is unavailable
    """
    if not agent:
        logger.error("Agent not available for analysis")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analysis service is currently unavailable"
        )
    
    try:
        logger.info(f"Processing analysis request: {request.query[:50]}...")
        
        result = await agent.analyze(request.query, request.context)
        
        logger.info("Analysis completed successfully")
        return QueryResponse(
            response=result["response"],
            analysis=result.get("analysis", {}),
            sources=result.get("sources", [])
        )
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e.message}"
        )
    except AgentExecutionError as e:
        logger.error(f"Agent execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis execution failed: {e.message}"
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Health status and agent availability
    """
    from datetime import datetime
    
    return HealthResponse(
        status="healthy" if agent else "degraded",
        agent_available=agent is not None,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
