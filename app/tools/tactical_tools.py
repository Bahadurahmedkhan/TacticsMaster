"""
Tactical Analysis Tools for Tactics Master Agent

This module contains analytical tools for processing cricket data and generating
tactical insights. These tools perform the core analysis logic for identifying
weaknesses, matchups, and strategic recommendations.

Author: Tactics Master Team
Version: 1.0.0
"""

# Standard library imports
import json
import logging
from typing import Dict, List, Any, Optional

# Third-party imports
from langchain.tools import tool
from pydantic import BaseModel, Field

# Local imports
from exceptions import (
    DataValidationError,
    DataProcessingError,
    AnalysisError
)

# Configure logging
logger = logging.getLogger(__name__)

class WeaknessAnalysisInput(BaseModel):
    """Input schema for analyze_weaknesses tool"""
    player_data: str = Field(description="JSON string containing player data to analyze")

class MatchupAnalysisInput(BaseModel):
    """Input schema for find_best_matchup tool"""
    player1_data: str = Field(description="JSON string containing first player data")
    player2_data: str = Field(description="JSON string containing second player data")

class BowlingPlanInput(BaseModel):
    """Input schema for generate_bowling_plan tool"""
    player_data: str = Field(description="JSON string containing player data")
    context: str = Field(description="Context for the bowling plan (e.g., match situation)")

class FieldingPlanInput(BaseModel):
    """Input schema for generate_fielding_plan tool"""
    player_data: str = Field(description="JSON string containing player data")
    bowling_plan: str = Field(description="JSON string containing bowling plan")

@tool(args_schema=WeaknessAnalysisInput)
def analyze_weaknesses(player_data: str) -> str:
    """
    Analyze player vulnerabilities and patterns.
    
    This tool processes player data to identify:
    - Batting weaknesses against specific bowling types
    - Vulnerable phases of innings
    - Performance patterns and trends
    - Areas for tactical exploitation
    
    Args:
        player_data: JSON string containing player statistics and form
        
    Returns:
        str: JSON string containing weakness analysis
        
    Raises:
        json.JSONDecodeError: If player_data is not valid JSON
        Exception: If analysis fails
    """
    if not player_data or not player_data.strip():
        logger.warning("Empty player data provided")
        raise DataValidationError(
            message="Player data cannot be empty",
            error_code="EMPTY_PLAYER_DATA",
            context={"data_length": len(player_data) if player_data else 0}
        )
    
    try:
        logger.info("Starting weakness analysis")
        
        # Parse the input data
        data = json.loads(player_data)
        
        # Perform weakness analysis
        analysis = {
            "player_name": data.get("player_name", "Unknown"),
            "overall_assessment": _assess_player_overall(data),
            "key_weaknesses": _identify_weaknesses(data),
            "vulnerable_phases": _identify_vulnerable_phases(data),
            "tactical_opportunities": _identify_tactical_opportunities(data),
            "recommendations": _generate_weakness_recommendations(data)
        }
        
        logger.info("Weakness analysis completed successfully")
        return json.dumps(analysis, indent=2)
        
    except DataValidationError:
        # Re-raise validation errors
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in player data: {e}")
        raise DataValidationError(
            message="Invalid player data format - JSON decode error",
            error_code="INVALID_JSON_DATA",
            context={"json_error": str(e), "data_preview": player_data[:100]}
        )
    except Exception as e:
        logger.error(f"Weakness analysis failed: {e}")
        raise AnalysisError(
            message=f"Weakness analysis failed: {str(e)}",
            error_code="WEAKNESS_ANALYSIS_ERROR",
            context={"original_error": str(e), "data_preview": player_data[:100]}
        )

@tool(args_schema=MatchupAnalysisInput)
def find_best_matchup(player1_data: str, player2_data: str) -> str:
    """
    Identify optimal player vs player matchups.
    
    This tool analyzes two players to determine:
    - Which player has the advantage
    - Key factors in the matchup
    - Tactical considerations
    - Strategic recommendations
    
    Args:
        player1_data: JSON string containing first player data
        player2_data: JSON string containing second player data
        
    Returns:
        str: JSON string containing matchup analysis
    """
    try:
        # Parse the input data
        data1 = json.loads(player1_data)
        data2 = json.loads(player2_data)
        
        # Perform matchup analysis
        analysis = {
            "player1": data1.get("player_name", "Player 1"),
            "player2": data2.get("player_name", "Player 2"),
            "matchup_assessment": _assess_matchup(data1, data2),
            "key_factors": _identify_key_factors(data1, data2),
            "tactical_considerations": _generate_tactical_considerations(data1, data2),
            "recommendations": _generate_matchup_recommendations(data1, data2)
        }
        
        return json.dumps(analysis, indent=2)
        
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid player data format",
            "analysis": {}
        })
    except Exception as e:
        return json.dumps({
            "error": f"Matchup analysis failed: {str(e)}",
            "analysis": {}
        })

@tool(args_schema=BowlingPlanInput)
def generate_bowling_plan(player_data: str, context: str) -> str:
    """
    Create specific bowling strategies against a player.
    
    This tool generates detailed bowling plans including:
    - Bowling phases and strategies
    - Field placements for each phase
    - Key bowlers to use
    - Tactical variations and changes
    
    Args:
        player_data: JSON string containing player data
        context: Context for the bowling plan
        
    Returns:
        str: JSON string containing bowling plan
    """
    try:
        # Parse the input data
        data = json.loads(player_data)
        
        # Generate bowling plan
        plan = {
            "player_name": data.get("player_name", "Unknown"),
            "context": context,
            "overall_strategy": _generate_overall_strategy(data, context),
            "phase_plans": _generate_phase_plans(data),
            "field_placements": _generate_field_placements(data),
            "bowler_assignments": _generate_bowler_assignments(data),
            "tactical_variations": _generate_tactical_variations(data)
        }
        
        return json.dumps(plan, indent=2)
        
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid player data format",
            "plan": {}
        })
    except Exception as e:
        return json.dumps({
            "error": f"Bowling plan generation failed: {str(e)}",
            "plan": {}
        })

@tool(args_schema=FieldingPlanInput)
def generate_fielding_plan(player_data: str, bowling_plan: str) -> str:
    """
    Design fielding setups and positions.
    
    This tool creates detailed fielding plans including:
    - Field placements for different phases
    - Key fielding positions
    - Tactical adjustments
    - Communication strategies
    
    Args:
        player_data: JSON string containing player data
        bowling_plan: JSON string containing bowling plan
        
    Returns:
        str: JSON string containing fielding plan
    """
    try:
        # Parse the input data
        data = json.loads(player_data)
        plan = json.loads(bowling_plan)
        
        # Generate fielding plan
        fielding_plan = {
            "player_name": data.get("player_name", "Unknown"),
            "overall_approach": _generate_fielding_approach(data, plan),
            "phase_fielding": _generate_phase_fielding(data, plan),
            "key_positions": _identify_key_positions(data, plan),
            "tactical_adjustments": _generate_fielding_adjustments(data, plan),
            "communication_points": _generate_communication_points(data, plan)
        }
        
        return json.dumps(fielding_plan, indent=2)
        
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid data format",
            "plan": {}
        })
    except Exception as e:
        return json.dumps({
            "error": f"Fielding plan generation failed: {str(e)}",
            "plan": {}
        })

# Helper functions for analysis logic

def _assess_player_overall(data: Dict[str, Any]) -> str:
    """Assess overall player performance"""
    recent_form = data.get("recent_form", {})
    avg = recent_form.get("batting_average", 0)
    sr = recent_form.get("strike_rate", 0)
    
    if avg > 50 and sr > 120:
        return "Excellent form - key player in good touch"
    elif avg > 40 and sr > 110:
        return "Good form - reliable performer"
    elif avg > 30:
        return "Moderate form - needs support"
    else:
        return "Poor form - consider alternatives"

def _identify_weaknesses(data: Dict[str, Any]) -> List[str]:
    """Identify key weaknesses"""
    weaknesses = []
    
    # Analyze weaknesses from data
    weakness_data = data.get("weaknesses", {})
    
    if "against_spin" in weakness_data:
        spin_data = weakness_data["against_spin"]
        if spin_data.get("average", 0) < 30:
            weaknesses.append(f"Vulnerable against spin bowling (avg: {spin_data.get('average', 0)})")
    
    if "early_innings" in weakness_data:
        early_data = weakness_data["early_innings"]
        if early_data.get("first_10_balls", {}).get("average", 0) < 20:
            weaknesses.append("Slow starter - target early in innings")
    
    return weaknesses

def _identify_vulnerable_phases(data: Dict[str, Any]) -> List[str]:
    """Identify vulnerable phases of innings"""
    phases = []
    
    # Analyze different phases
    if data.get("recent_form", {}).get("strike_rate", 0) < 100:
        phases.append("Struggles in powerplay overs")
    
    if data.get("weaknesses", {}).get("early_innings"):
        phases.append("Vulnerable in first 10 balls")
    
    return phases

def _identify_tactical_opportunities(data: Dict[str, Any]) -> List[str]:
    """Identify tactical opportunities"""
    opportunities = []
    
    # Analyze strengths to find counter-opportunities
    strengths = data.get("strengths", {})
    
    if "death_overs" in strengths:
        opportunities.append("Avoid bowling in death overs - bowl out early")
    
    if "against_pace" in strengths:
        opportunities.append("Use spin bowling to counter pace strength")
    
    return opportunities

def _generate_weakness_recommendations(data: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on weaknesses"""
    recommendations = []
    
    weaknesses = data.get("weaknesses", {})
    
    if "against_spin" in weaknesses:
        recommendations.append("Use spin bowling, especially in middle overs")
    
    if "early_innings" in weaknesses:
        recommendations.append("Attack early with pace - first 10 balls crucial")
    
    return recommendations

def _assess_matchup(data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
    """Assess player vs player matchup"""
    # Simple assessment based on recent form
    form1 = data1.get("recent_form", {}).get("batting_average", 0)
    form2 = data2.get("recent_form", {}).get("batting_average", 0)
    
    if form1 > form2 * 1.2:
        return f"{data1.get('player_name', 'Player 1')} has significant advantage"
    elif form2 > form1 * 1.2:
        return f"{data2.get('player_name', 'Player 2')} has significant advantage"
    else:
        return "Evenly matched - tactical execution crucial"

def _identify_key_factors(data1: Dict[str, Any], data2: Dict[str, Any]) -> List[str]:
    """Identify key factors in the matchup"""
    factors = []
    
    # Compare strengths and weaknesses
    if data1.get("strengths", {}).get("against_pace") and data2.get("weaknesses", {}).get("against_spin"):
        factors.append("Player 1's pace strength vs Player 2's spin weakness")
    
    return factors

def _generate_tactical_considerations(data1: Dict[str, Any], data2: Dict[str, Any]) -> List[str]:
    """Generate tactical considerations for the matchup"""
    considerations = []
    
    # Analyze tactical aspects
    considerations.append("Focus on exploiting identified weaknesses")
    considerations.append("Use field placements to support bowling strategy")
    
    return considerations

def _generate_matchup_recommendations(data1: Dict[str, Any], data2: Dict[str, Any]) -> List[str]:
    """Generate matchup-specific recommendations"""
    recommendations = []
    
    # Generate recommendations based on analysis
    recommendations.append("Target identified weaknesses with appropriate bowling")
    recommendations.append("Use field placements to create pressure")
    
    return recommendations

def _generate_overall_strategy(data: Dict[str, Any], context: str) -> str:
    """Generate overall bowling strategy"""
    return f"Attack early with pace bowling, use spin in middle overs, avoid death overs if possible"

def _generate_phase_plans(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate phase-specific bowling plans"""
    return {
        "powerplay": {
            "strategy": "Attack with pace bowling",
            "field_setting": "Attacking field with slips and gully",
            "key_bowlers": ["Fast bowlers with swing/seam"]
        },
        "middle_overs": {
            "strategy": "Use spin bowling to build pressure",
            "field_setting": "Close-in fielders, deep mid-wicket",
            "key_bowlers": ["Spinners with good control"]
        },
        "death_overs": {
            "strategy": "Avoid if possible - use variations",
            "field_setting": "Defensive field with boundary protection",
            "key_bowlers": ["Specialist death bowlers only"]
        }
    }

def _generate_field_placements(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate field placements for different phases"""
    return {
        "powerplay": ["Slip cordon", "Gully", "Short leg"],
        "middle_overs": ["Short mid-wicket", "Deep square leg", "Deep mid-wicket"],
        "death_overs": ["Long on", "Long off", "Deep mid-wicket"]
    }

def _generate_bowler_assignments(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Generate bowler assignments for different phases"""
    return {
        "powerplay": ["Opening fast bowlers"],
        "middle_overs": ["Spinners", "Medium pacers"],
        "death_overs": ["Specialist death bowlers"]
    }

def _generate_tactical_variations(data: Dict[str, Any]) -> List[str]:
    """Generate tactical variations"""
    return [
        "Change bowling angles",
        "Use slower balls and cutters",
        "Vary field placements based on situation"
    ]

def _generate_fielding_approach(data: Dict[str, Any], plan: Dict[str, Any]) -> str:
    """Generate overall fielding approach"""
    return "Aggressive fielding with close-in fielders for early wickets"

def _generate_phase_fielding(data: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    """Generate phase-specific fielding"""
    return {
        "powerplay": {
            "field_setting": "Attacking with slips, gully, and close-in fielders",
            "key_positions": ["Slip cordon", "Gully", "Short leg"]
        },
        "middle_overs": {
            "field_setting": "Balanced with close-in and boundary protection",
            "key_positions": ["Short mid-wicket", "Deep square leg", "Deep mid-wicket"]
        },
        "death_overs": {
            "field_setting": "Defensive with boundary protection",
            "key_positions": ["Long on", "Long off", "Deep mid-wicket"]
        }
    }

def _identify_key_positions(data: Dict[str, Any], plan: Dict[str, Any]) -> List[str]:
    """Identify key fielding positions"""
    return ["Slip cordon", "Gully", "Short leg", "Deep mid-wicket"]

def _generate_fielding_adjustments(data: Dict[str, Any], plan: Dict[str, Any]) -> List[str]:
    """Generate fielding adjustments"""
    return [
        "Adjust based on bowling type",
        "Move fielders based on player's scoring areas",
        "Use fielders to create pressure"
    ]

def _generate_communication_points(data: Dict[str, Any], plan: Dict[str, Any]) -> List[str]:
    """Generate communication points"""
    return [
        "Keep fielders alert for early wickets",
        "Communicate bowling changes clearly",
        "Maintain pressure through field placements"
    ]
