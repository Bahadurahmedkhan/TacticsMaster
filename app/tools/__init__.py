"""
Tactics Master Tools Package

This package contains all the custom tools for the Tactics Master agent.
It includes both API tools for fetching cricket data and tactical tools
for analysis and strategy generation.
"""

from .cricket_api_tools import (
    get_player_stats,
    get_team_squad,
    get_matchup_data,
    get_venue_stats
)

from .tactical_tools import (
    analyze_weaknesses,
    find_best_matchup,
    generate_bowling_plan,
    generate_fielding_plan
)

__all__ = [
    # API Tools
    "get_player_stats",
    "get_team_squad", 
    "get_matchup_data",
    "get_venue_stats",
    # Tactical Tools
    "analyze_weaknesses",
    "find_best_matchup",
    "generate_bowling_plan",
    "generate_fielding_plan"
]
