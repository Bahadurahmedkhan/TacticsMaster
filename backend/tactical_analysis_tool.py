import json
from typing import Dict, List, Any
import re

class TacticalAnalysisTool:
    """
    Tool for performing tactical analysis on cricket data
    """
    
    def analyze(self, data: str) -> str:
        """
        Analyze cricket data and provide tactical insights
        
        Args:
            data: JSON string containing cricket data
            
        Returns:
            JSON string containing tactical analysis
        """
        try:
            # Parse the input data
            cricket_data = json.loads(data)
            
            # Perform different types of analysis based on data structure
            if "player_name" in cricket_data:
                return self._analyze_player(cricket_data)
            elif "team_name" in cricket_data:
                return self._analyze_team(cricket_data)
            elif "head_to_head" in cricket_data:
                return self._analyze_matchup(cricket_data)
            else:
                return self._analyze_general(cricket_data)
                
        except json.JSONDecodeError:
            return json.dumps({
                "error": "Invalid data format",
                "analysis": {}
            })
        except Exception as e:
            return json.dumps({
                "error": f"Analysis failed: {str(e)}",
                "analysis": {}
            })
    
    def _analyze_player(self, data: Dict[str, Any]) -> str:
        """Analyze individual player data"""
        analysis = {
            "player_analysis": {
                "name": data.get("player_name", "Unknown"),
                "overall_assessment": self._assess_player_overall(data),
                "key_insights": self._extract_player_insights(data),
                "tactical_recommendations": self._generate_player_recommendations(data),
                "bowling_plan": self._create_bowling_plan(data),
                "fielding_plan": self._create_fielding_plan(data)
            }
        }
        
        return json.dumps(analysis, indent=2)
    
    def _analyze_team(self, data: Dict[str, Any]) -> str:
        """Analyze team data"""
        analysis = {
            "team_analysis": {
                "team_name": data.get("team_name", "Unknown"),
                "overall_assessment": self._assess_team_overall(data),
                "key_insights": self._extract_team_insights(data),
                "tactical_recommendations": self._generate_team_recommendations(data),
                "matchup_strategy": self._create_matchup_strategy(data)
            }
        }
        
        return json.dumps(analysis, indent=2)
    
    def _analyze_matchup(self, data: Dict[str, Any]) -> str:
        """Analyze head-to-head matchup data"""
        analysis = {
            "matchup_analysis": {
                "historical_performance": self._analyze_historical_performance(data),
                "venue_insights": self._analyze_venue_factors(data),
                "key_trends": self._identify_key_trends(data),
                "strategic_recommendations": self._generate_matchup_recommendations(data)
            }
        }
        
        return json.dumps(analysis, indent=2)
    
    def _analyze_general(self, data: Dict[str, Any]) -> str:
        """Analyze general cricket data"""
        analysis = {
            "general_analysis": {
                "data_summary": "General cricket data analysis",
                "insights": ["Data available for analysis", "Multiple data types supported"],
                "recommendations": ["Specify player, team, or matchup for detailed analysis"]
            }
        }
        
        return json.dumps(analysis, indent=2)
    
    def _assess_player_overall(self, data: Dict[str, Any]) -> str:
        """Assess overall player performance"""
        recent_form = data.get("recent_form", {})
        avg = recent_form.get("average", 0)
        sr = recent_form.get("strike_rate", 0)
        
        if avg > 50 and sr > 120:
            return "Excellent form - key player in good touch"
        elif avg > 40 and sr > 110:
            return "Good form - reliable performer"
        elif avg > 30:
            return "Moderate form - needs support"
        else:
            return "Poor form - consider alternatives"
    
    def _extract_player_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract key insights about the player"""
        insights = []
        
        # Analyze weaknesses
        weaknesses = data.get("weaknesses", {})
        if "against_spin" in weaknesses:
            spin_data = weaknesses["against_spin"]
            if spin_data.get("average", 0) < 30:
                insights.append(f"Vulnerable against spin bowling (avg: {spin_data.get('average', 0)})")
        
        if "early_innings" in weaknesses:
            early_data = weaknesses["early_innings"]
            if early_data.get("first_10_balls", {}).get("average", 0) < 20:
                insights.append("Slow starter - target early in innings")
        
        # Analyze strengths
        strengths = data.get("strengths", {})
        if "death_overs" in strengths:
            death_data = strengths["death_overs"]
            if death_data.get("overs_16_20", {}).get("strike_rate", 0) > 140:
                insights.append("Dangerous in death overs - bowl out early")
        
        return insights
    
    def _generate_player_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate tactical recommendations for the player"""
        recommendations = []
        
        weaknesses = data.get("weaknesses", {})
        strengths = data.get("strengths", {})
        
        # Bowling recommendations
        if "against_spin" in weaknesses:
            recommendations.append("Use spin bowling, especially in middle overs")
        
        if "early_innings" in weaknesses:
            recommendations.append("Attack early with pace - first 10 balls crucial")
        
        if "death_overs" in strengths:
            recommendations.append("Avoid bowling in death overs - bowl out before overs 16-20")
        
        # Fielding recommendations
        recommendations.append("Set attacking field for early wickets")
        recommendations.append("Use close-in fielders for spin bowling")
        
        return recommendations
    
    def _create_bowling_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a specific bowling plan"""
        return {
            "early_overs": {
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
    
    def _create_fielding_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fielding plan"""
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
    
    def _assess_team_overall(self, data: Dict[str, Any]) -> str:
        """Assess overall team performance"""
        performance = data.get("recent_performance", {})
        win_pct = performance.get("win_percentage", 0)
        
        if win_pct > 70:
            return "Strong team in excellent form"
        elif win_pct > 50:
            return "Competitive team with good potential"
        else:
            return "Struggling team - opportunities available"
    
    def _extract_team_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract team insights"""
        insights = []
        
        strengths = data.get("strengths", [])
        weaknesses = data.get("weaknesses", [])
        
        for strength in strengths:
            insights.append(f"Team strength: {strength}")
        
        for weakness in weaknesses:
            insights.append(f"Team weakness: {weakness}")
        
        return insights
    
    def _generate_team_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate team-level recommendations"""
        recommendations = []
        
        weaknesses = data.get("weaknesses", [])
        
        for weakness in weaknesses:
            if "middle order" in weakness.lower():
                recommendations.append("Target middle order with spin bowling")
            elif "death bowling" in weakness.lower():
                recommendations.append("Attack in death overs with aggressive batting")
            elif "top order" in weakness.lower():
                recommendations.append("Focus on early wickets to expose middle order")
        
        return recommendations
    
    def _create_matchup_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create matchup strategy"""
        return {
            "overall_approach": "Aggressive batting and disciplined bowling",
            "key_focus_areas": [
                "Early wickets to build pressure",
                "Target opponent's weak bowling options",
                "Maintain run rate throughout innings"
            ],
            "risk_management": [
                "Avoid unnecessary risks in middle overs",
                "Consolidate after early wickets",
                "Accelerate in death overs"
            ]
        }
    
    def _analyze_historical_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze historical performance"""
        h2h = data.get("head_to_head", {})
        return {
            "win_percentage": h2h.get("win_percentage", 0),
            "total_matches": h2h.get("total_matches", 0),
            "recent_trend": "Favorable" if h2h.get("win_percentage", 0) > 50 else "Unfavorable"
        }
    
    def _analyze_venue_factors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze venue-specific factors"""
        venue_analysis = data.get("venue_analysis", {})
        return {
            "pitch_conditions": venue_analysis.get("pitch_type", "Unknown"),
            "average_score": venue_analysis.get("average_score", 0),
            "venue_advantage": "Favorable" if venue_analysis.get("india_wins", 0) > venue_analysis.get("matches_played", 1) * 0.5 else "Neutral"
        }
    
    def _identify_key_trends(self, data: Dict[str, Any]) -> List[str]:
        """Identify key trends from historical data"""
        trends = []
        
        recent_matches = data.get("recent_encounters", [])
        if len(recent_matches) >= 2:
            wins = sum(1 for match in recent_matches if "won" in match.get("result", "").lower())
            if wins >= len(recent_matches) * 0.7:
                trends.append("Strong recent form against this opponent")
            elif wins <= len(recent_matches) * 0.3:
                trends.append("Struggling against this opponent recently")
        
        return trends
    
    def _generate_matchup_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate matchup-specific recommendations"""
        recommendations = []
        
        h2h = data.get("head_to_head", {})
        win_pct = h2h.get("win_percentage", 0)
        
        if win_pct > 60:
            recommendations.append("Maintain aggressive approach - historical advantage")
        elif win_pct < 40:
            recommendations.append("Focus on key matchups and exploit weaknesses")
        else:
            recommendations.append("Balanced approach - focus on execution")
        
        return recommendations
