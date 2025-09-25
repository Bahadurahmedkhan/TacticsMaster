import json
from typing import Dict, List, Any
from datetime import datetime

class ResponseGenerationTool:
    """
    Tool for formatting tactical analysis into coach-friendly responses
    """
    
    def format_response(self, analysis: str) -> str:
        """
        Format tactical analysis into a structured, coach-friendly response
        
        Args:
            analysis: JSON string containing tactical analysis
            
        Returns:
            Formatted response string
        """
        try:
            # Parse the analysis data
            analysis_data = json.loads(analysis)
            
            # Generate formatted response based on analysis type
            if "player_analysis" in analysis_data:
                return self._format_player_response(analysis_data["player_analysis"])
            elif "team_analysis" in analysis_data:
                return self._format_team_response(analysis_data["team_analysis"])
            elif "matchup_analysis" in analysis_data:
                return self._format_matchup_response(analysis_data["matchup_analysis"])
            else:
                return self._format_general_response(analysis_data)
                
        except json.JSONDecodeError:
            return "Error: Unable to parse analysis data"
        except Exception as e:
            return f"Error: Failed to format response - {str(e)}"
    
    def _format_player_response(self, analysis: Dict[str, Any]) -> str:
        """Format player analysis response"""
        player_name = analysis.get("name", "Player")
        
        response = f"# 🏏 Tactical Analysis: {player_name}\n\n"
        
        # Overall Assessment
        response += f"## 📊 Overall Assessment\n"
        response += f"{analysis.get('overall_assessment', 'No assessment available')}\n\n"
        
        # Key Insights
        insights = analysis.get("key_insights", [])
        if insights:
            response += f"## 🔍 Key Insights\n"
            for i, insight in enumerate(insights, 1):
                response += f"{i}. {insight}\n"
            response += "\n"
        
        # Tactical Recommendations
        recommendations = analysis.get("tactical_recommendations", [])
        if recommendations:
            response += f"## 🎯 Tactical Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
            response += "\n"
        
        # Bowling Plan
        bowling_plan = analysis.get("bowling_plan", {})
        if bowling_plan:
            response += f"## 🏏 Bowling Plan\n"
            for phase, plan in bowling_plan.items():
                response += f"### {phase.replace('_', ' ').title()}\n"
                response += f"**Strategy:** {plan.get('strategy', 'N/A')}\n"
                response += f"**Field Setting:** {plan.get('field_setting', 'N/A')}\n"
                response += f"**Key Bowlers:** {plan.get('key_bowlers', 'N/A')}\n\n"
        
        # Fielding Plan
        fielding_plan = analysis.get("fielding_plan", {})
        if fielding_plan:
            response += f"## 🏃‍♂️ Fielding Plan\n"
            for phase, plan in fielding_plan.items():
                response += f"### {phase.replace('_', ' ').title()}\n"
                response += f"**Field Setting:** {plan.get('field_setting', 'N/A')}\n"
                response += f"**Key Positions:** {', '.join(plan.get('key_positions', []))}\n\n"
        
        # Add timestamp
        response += f"---\n*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return response
    
    def _format_team_response(self, analysis: Dict[str, Any]) -> str:
        """Format team analysis response"""
        team_name = analysis.get("team_name", "Team")
        
        response = f"# 🏏 Team Analysis: {team_name}\n\n"
        
        # Overall Assessment
        response += f"## 📊 Overall Assessment\n"
        response += f"{analysis.get('overall_assessment', 'No assessment available')}\n\n"
        
        # Key Insights
        insights = analysis.get("key_insights", [])
        if insights:
            response += f"## 🔍 Key Insights\n"
            for i, insight in enumerate(insights, 1):
                response += f"{i}. {insight}\n"
            response += "\n"
        
        # Tactical Recommendations
        recommendations = analysis.get("tactical_recommendations", [])
        if recommendations:
            response += f"## 🎯 Tactical Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
            response += "\n"
        
        # Matchup Strategy
        strategy = analysis.get("matchup_strategy", {})
        if strategy:
            response += f"## 🎯 Matchup Strategy\n"
            response += f"**Overall Approach:** {strategy.get('overall_approach', 'N/A')}\n\n"
            
            focus_areas = strategy.get("key_focus_areas", [])
            if focus_areas:
                response += f"**Key Focus Areas:**\n"
                for i, area in enumerate(focus_areas, 1):
                    response += f"{i}. {area}\n"
                response += "\n"
            
            risk_management = strategy.get("risk_management", [])
            if risk_management:
                response += f"**Risk Management:**\n"
                for i, risk in enumerate(risk_management, 1):
                    response += f"{i}. {risk}\n"
                response += "\n"
        
        # Add timestamp
        response += f"---\n*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return response
    
    def _format_matchup_response(self, analysis: Dict[str, Any]) -> str:
        """Format matchup analysis response"""
        response = f"# 🏏 Matchup Analysis\n\n"
        
        # Historical Performance
        historical = analysis.get("historical_performance", {})
        if historical:
            response += f"## 📈 Historical Performance\n"
            response += f"**Win Percentage:** {historical.get('win_percentage', 0)}%\n"
            response += f"**Total Matches:** {historical.get('total_matches', 0)}\n"
            response += f"**Recent Trend:** {historical.get('recent_trend', 'N/A')}\n\n"
        
        # Venue Insights
        venue = analysis.get("venue_insights", {})
        if venue:
            response += f"## 🏟️ Venue Insights\n"
            response += f"**Pitch Conditions:** {venue.get('pitch_conditions', 'N/A')}\n"
            response += f"**Average Score:** {venue.get('average_score', 0)}\n"
            response += f"**Venue Advantage:** {venue.get('venue_advantage', 'N/A')}\n\n"
        
        # Key Trends
        trends = analysis.get("key_trends", [])
        if trends:
            response += f"## 📊 Key Trends\n"
            for i, trend in enumerate(trends, 1):
                response += f"{i}. {trend}\n"
            response += "\n"
        
        # Strategic Recommendations
        recommendations = analysis.get("strategic_recommendations", [])
        if recommendations:
            response += f"## 🎯 Strategic Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
            response += "\n"
        
        # Add timestamp
        response += f"---\n*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return response
    
    def _format_general_response(self, analysis: Dict[str, Any]) -> str:
        """Format general analysis response"""
        response = f"# 🏏 Cricket Analysis\n\n"
        
        data_summary = analysis.get("data_summary", "General analysis")
        response += f"## 📋 Summary\n{data_summary}\n\n"
        
        insights = analysis.get("insights", [])
        if insights:
            response += f"## 🔍 Insights\n"
            for i, insight in enumerate(insights, 1):
                response += f"{i}. {insight}\n"
            response += "\n"
        
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            response += f"## 🎯 Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
            response += "\n"
        
        # Add timestamp
        response += f"---\n*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return response
