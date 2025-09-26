"""
Request Models for Tactics Master API

This module defines comprehensive request models with validation,
documentation, and examples for all API endpoints.

Author: Tactics Master Team
Version: 2.0.0
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum

from ...core.validation import Validator


class AnalysisType(str, Enum):
    """Analysis type enumeration"""
    COMPREHENSIVE = "comprehensive"
    PLAYER = "player"
    TEAM = "team"
    MATCHUP = "matchup"
    VENUE = "venue"
    TACTICAL = "tactical"


class Priority(str, Enum):
    """Priority level enumeration"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class AnalysisRequest(BaseModel):
    """
    Request model for cricket tactical analysis.
    
    This model defines the structure for analysis requests with comprehensive
    validation and documentation.
    """
    
    query: str = Field(
        ...,
        description="The cricket analysis query",
        min_length=1,
        max_length=2000,
        example="Analyze Virat Kohli's batting performance against spin bowling in recent matches",
        title="Analysis Query"
    )
    
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the analysis",
        example={
            "team": "India",
            "format": "ODI",
            "venue": "Wankhede Stadium",
            "opponent": "Australia",
            "match_situation": "chasing 300+ target"
        },
        title="Analysis Context"
    )
    
    analysis_type: AnalysisType = Field(
        default=AnalysisType.COMPREHENSIVE,
        description="Type of analysis to perform",
        example="comprehensive",
        title="Analysis Type"
    )
    
    include_recommendations: bool = Field(
        default=True,
        description="Whether to include tactical recommendations",
        example=True,
        title="Include Recommendations"
    )
    
    include_statistics: bool = Field(
        default=True,
        description="Whether to include statistical analysis",
        example=True,
        title="Include Statistics"
    )
    
    include_visualizations: bool = Field(
        default=False,
        description="Whether to include data visualizations",
        example=False,
        title="Include Visualizations"
    )
    
    priority: Priority = Field(
        default=Priority.NORMAL,
        description="Analysis priority level",
        example="normal",
        title="Priority Level"
    )
    
    max_processing_time: Optional[int] = Field(
        default=None,
        description="Maximum processing time in seconds",
        ge=10,
        le=300,
        example=60,
        title="Max Processing Time"
    )
    
    language: str = Field(
        default="en",
        description="Response language",
        regex="^(en|hi|es|fr|de|it|pt|ru|zh|ja|ko)$",
        example="en",
        title="Response Language"
    )
    
    @validator('query')
    def validate_query(cls, v):
        """Validate analysis query"""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        
        # Sanitize query
        sanitized = Validator.validate_string(
            value=v.strip(),
            required=True,
            min_length=1,
            max_length=2000,
            field_name="query"
        )
        
        # Check for malicious content
        if any(word in sanitized.lower() for word in ['<script', 'javascript:', 'onload=']):
            raise ValueError("Query contains potentially malicious content")
        
        return sanitized
    
    @validator('context')
    def validate_context(cls, v):
        """Validate analysis context"""
        if not isinstance(v, dict):
            raise ValueError("Context must be a dictionary")
        
        # Validate context size
        context_str = str(v)
        if len(context_str) > 10000:  # 10KB limit
            raise ValueError("Context too large (max 10KB)")
        
        # Validate context keys
        allowed_keys = {
            'team', 'opponent', 'format', 'venue', 'match_situation',
            'player_name', 'bowler_name', 'batsman_name', 'conditions',
            'pitch_type', 'weather', 'toss_winner', 'target_score'
        }
        
        for key in v.keys():
            if not isinstance(key, str):
                raise ValueError("Context keys must be strings")
            if key not in allowed_keys:
                raise ValueError(f"Invalid context key: {key}")
        
        return v
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        """Validate analysis type"""
        if v not in [e.value for e in AnalysisType]:
            raise ValueError(f"Invalid analysis type: {v}")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        """Validate priority level"""
        if v not in [e.value for e in Priority]:
            raise ValueError(f"Invalid priority: {v}")
        return v
    
    @root_validator
    def validate_request(cls, values):
        """Validate entire request"""
        query = values.get('query', '')
        analysis_type = values.get('analysis_type')
        
        # Validate query matches analysis type
        if analysis_type == AnalysisType.PLAYER:
            if not any(word in query.lower() for word in ['player', 'batsman', 'bowler', 'name']):
                raise ValueError("Player analysis requires player-related query")
        
        elif analysis_type == AnalysisType.TEAM:
            if not any(word in query.lower() for word in ['team', 'squad', 'lineup']):
                raise ValueError("Team analysis requires team-related query")
        
        elif analysis_type == AnalysisType.MATCHUP:
            if not any(word in query.lower() for word in ['vs', 'against', 'matchup', 'head to head']):
                raise ValueError("Matchup analysis requires head-to-head query")
        
        return values
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Analyze Virat Kohli's performance against spin bowling in recent ODIs",
                "context": {
                    "team": "India",
                    "format": "ODI",
                    "venue": "Wankhede Stadium",
                    "opponent": "Australia"
                },
                "analysis_type": "player",
                "include_recommendations": True,
                "include_statistics": True,
                "priority": "normal",
                "language": "en"
            }
        }


class BatchAnalysisRequest(BaseModel):
    """
    Request model for batch cricket analysis.
    
    This model defines the structure for batch analysis requests with
    multiple queries.
    """
    
    queries: List[AnalysisRequest] = Field(
        ...,
        description="List of analysis requests",
        min_items=1,
        max_items=10,
        title="Analysis Queries"
    )
    
    batch_id: Optional[str] = Field(
        default=None,
        description="Optional batch identifier",
        max_length=100,
        example="batch_2024_001",
        title="Batch ID"
    )
    
    parallel: bool = Field(
        default=True,
        description="Whether to process queries in parallel",
        example=True,
        title="Parallel Processing"
    )
    
    max_batch_time: Optional[int] = Field(
        default=None,
        description="Maximum batch processing time in seconds",
        ge=30,
        le=600,
        example=300,
        title="Max Batch Time"
    )
    
    @validator('queries')
    def validate_queries(cls, v):
        """Validate batch queries"""
        if not v:
            raise ValueError("At least one query is required")
        
        if len(v) > 10:
            raise ValueError("Maximum 10 queries allowed per batch")
        
        # Check for duplicate queries
        query_texts = [q.query for q in v]
        if len(query_texts) != len(set(query_texts)):
            raise ValueError("Duplicate queries not allowed in batch")
        
        return v
    
    @validator('batch_id')
    def validate_batch_id(cls, v):
        """Validate batch ID"""
        if v is not None:
            return Validator.validate_string(
                value=v,
                required=True,
                min_length=1,
                max_length=100,
                field_name="batch_id"
            )
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "queries": [
                    {
                        "query": "Analyze Virat Kohli's batting performance",
                        "analysis_type": "player",
                        "include_recommendations": True
                    },
                    {
                        "query": "Analyze India's bowling strategy",
                        "analysis_type": "team",
                        "include_statistics": True
                    }
                ],
                "batch_id": "batch_2024_001",
                "parallel": True,
                "max_batch_time": 300
            }
        }


class PlayerAnalysisRequest(BaseModel):
    """
    Request model for player-specific analysis.
    """
    
    player_name: str = Field(
        ...,
        description="Name of the player to analyze",
        min_length=1,
        max_length=100,
        example="Virat Kohli",
        title="Player Name"
    )
    
    analysis_focus: str = Field(
        default="comprehensive",
        description="Focus area for analysis",
        regex="^(batting|bowling|fielding|comprehensive|recent_form|career)$",
        example="batting",
        title="Analysis Focus"
    )
    
    time_period: str = Field(
        default="recent",
        description="Time period for analysis",
        regex="^(recent|last_year|career|last_5_matches|last_10_matches)$",
        example="recent",
        title="Time Period"
    )
    
    format: str = Field(
        default="all",
        description="Cricket format to analyze",
        regex="^(all|test|odi|t20|ipl)$",
        example="odi",
        title="Cricket Format"
    )
    
    @validator('player_name')
    def validate_player_name(cls, v):
        """Validate player name"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=100,
            field_name="player_name"
        )
    
    class Config:
        schema_extra = {
            "example": {
                "player_name": "Virat Kohli",
                "analysis_focus": "batting",
                "time_period": "recent",
                "format": "odi"
            }
        }


class TeamAnalysisRequest(BaseModel):
    """
    Request model for team-specific analysis.
    """
    
    team_name: str = Field(
        ...,
        description="Name of the team to analyze",
        min_length=1,
        max_length=100,
        example="India",
        title="Team Name"
    )
    
    analysis_type: str = Field(
        default="comprehensive",
        description="Type of team analysis",
        regex="^(comprehensive|batting|bowling|fielding|squad|tactics)$",
        example="comprehensive",
        title="Analysis Type"
    )
    
    format: str = Field(
        default="all",
        description="Cricket format to analyze",
        regex="^(all|test|odi|t20)$",
        example="odi",
        title="Cricket Format"
    )
    
    @validator('team_name')
    def validate_team_name(cls, v):
        """Validate team name"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=100,
            field_name="team_name"
        )
    
    class Config:
        schema_extra = {
            "example": {
                "team_name": "India",
                "analysis_type": "comprehensive",
                "format": "odi"
            }
        }


class MatchupAnalysisRequest(BaseModel):
    """
    Request model for head-to-head analysis.
    """
    
    team1: str = Field(
        ...,
        description="First team name",
        min_length=1,
        max_length=100,
        example="India",
        title="Team 1"
    )
    
    team2: str = Field(
        ...,
        description="Second team name",
        min_length=1,
        max_length=100,
        example="Australia",
        title="Team 2"
    )
    
    format: str = Field(
        default="all",
        description="Cricket format to analyze",
        regex="^(all|test|odi|t20)$",
        example="odi",
        title="Cricket Format"
    )
    
    time_period: str = Field(
        default="all",
        description="Time period for analysis",
        regex="^(all|last_year|last_5_matches|last_10_matches)$",
        example="all",
        title="Time Period"
    )
    
    @validator('team1', 'team2')
    def validate_team_names(cls, v):
        """Validate team names"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=100,
            field_name="team_name"
        )
    
    @root_validator
    def validate_teams_different(cls, values):
        """Validate teams are different"""
        team1 = values.get('team1', '').lower()
        team2 = values.get('team2', '').lower()
        
        if team1 == team2:
            raise ValueError("Team 1 and Team 2 must be different")
        
        return values
    
    class Config:
        schema_extra = {
            "example": {
                "team1": "India",
                "team2": "Australia",
                "format": "odi",
                "time_period": "last_year"
            }
        }


class VenueAnalysisRequest(BaseModel):
    """
    Request model for venue-specific analysis.
    """
    
    venue_name: str = Field(
        ...,
        description="Name of the venue to analyze",
        min_length=1,
        max_length=100,
        example="Wankhede Stadium",
        title="Venue Name"
    )
    
    analysis_focus: str = Field(
        default="comprehensive",
        description="Focus area for analysis",
        regex="^(comprehensive|pitch|weather|records|tactics)$",
        example="comprehensive",
        title="Analysis Focus"
    )
    
    format: str = Field(
        default="all",
        description="Cricket format to analyze",
        regex="^(all|test|odi|t20)$",
        example="odi",
        title="Cricket Format"
    )
    
    @validator('venue_name')
    def validate_venue_name(cls, v):
        """Validate venue name"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=100,
            field_name="venue_name"
        )
    
    class Config:
        schema_extra = {
            "example": {
                "venue_name": "Wankhede Stadium",
                "analysis_focus": "comprehensive",
                "format": "odi"
            }
        }


class TacticalPlanRequest(BaseModel):
    """
    Request model for tactical planning.
    """
    
    scenario: str = Field(
        ...,
        description="Tactical scenario to plan for",
        min_length=1,
        max_length=500,
        example="India vs Australia ODI at Wankhede Stadium",
        title="Tactical Scenario"
    )
    
    plan_type: str = Field(
        default="comprehensive",
        description="Type of tactical plan",
        regex="^(comprehensive|batting|bowling|fielding|powerplay|death_overs)$",
        example="comprehensive",
        title="Plan Type"
    )
    
    conditions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Match conditions and context",
        example={
            "pitch_type": "batting_friendly",
            "weather": "clear",
            "dew_factor": "high"
        },
        title="Match Conditions"
    )
    
    @validator('scenario')
    def validate_scenario(cls, v):
        """Validate tactical scenario"""
        return Validator.validate_string(
            value=v,
            required=True,
            min_length=1,
            max_length=500,
            field_name="scenario"
        )
    
    class Config:
        schema_extra = {
            "example": {
                "scenario": "India vs Australia ODI at Wankhede Stadium",
                "plan_type": "comprehensive",
                "conditions": {
                    "pitch_type": "batting_friendly",
                    "weather": "clear",
                    "dew_factor": "high"
                }
            }
        }
