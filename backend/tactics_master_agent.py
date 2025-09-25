import os
import json
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from cricket_data_tool import CricketDataTool
from tactical_analysis_tool import TacticalAnalysisTool
from response_generation_tool import ResponseGenerationTool

class TacticsMasterAgent:
    """
    A LangChain-based agent that provides cricket tactical analysis
    by orchestrating multiple tools to deliver comprehensive insights.
    """
    
    def __init__(self):
        # Initialize with real API keys
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.1,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Initialize tools
        self.cricket_data_tool = CricketDataTool()
        self.tactical_analysis_tool = TacticalAnalysisTool()
        self.response_generation_tool = ResponseGenerationTool()
        
        # Create the agent
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the LangChain agent with all tools"""
        
        # Define available tools
        tools = [
            Tool(
                name="get_cricket_data",
                description="Fetch cricket data including player stats, team information, and match history",
                func=self.cricket_data_tool.get_data
            ),
            Tool(
                name="analyze_tactics",
                description="Perform tactical analysis on cricket data to identify patterns and weaknesses",
                func=self.tactical_analysis_tool.analyze
            ),
            Tool(
                name="generate_response",
                description="Format tactical analysis into coach-friendly response",
                func=self.response_generation_tool.format_response
            )
        ]
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent
        agent = create_openai_tools_agent(self.llm, tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True
        )
    
    def _get_system_prompt(self):
        """Get the system prompt for the agent"""
        return """
        You are the Tactics Master, an expert cricket analyst AI that helps coaches make data-driven tactical decisions.
        
        Your role is to:
        1. Gather relevant cricket data (player stats, team info, match history)
        2. Analyze the data to identify tactical patterns and weaknesses
        3. Provide actionable insights and recommendations for coaches
        
        Always structure your analysis with:
        - Key findings from the data
        - Identified weaknesses or opportunities
        - Specific tactical recommendations
        - Fielding and bowling strategies
        
        Be concise but comprehensive. Focus on actionable insights that coaches can implement immediately.
        """
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a cricket tactics query and return comprehensive insights
        
        Args:
            query: The coach's question or request
            context: Additional context (team, match, etc.)
            
        Returns:
            Dictionary containing response, analysis, and sources
        """
        try:
            # Prepare input for the agent
            agent_input = {
                "input": query,
                "chat_history": [],
                "context": context or {}
            }
            
            # Run the agent
            result = self.agent.invoke(agent_input)
            
            # Extract response and intermediate steps
            response = result.get("output", "")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Process intermediate steps to extract analysis and sources
            analysis = self._extract_analysis(intermediate_steps)
            sources = self._extract_sources(intermediate_steps)
            
            return {
                "response": response,
                "analysis": analysis,
                "sources": sources
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error while analyzing your query: {str(e)}",
                "analysis": {},
                "sources": []
            }
    
    def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate a mock response for testing purposes"""
        
        query_lower = query.lower()
        
        if "batting" in query_lower or "batsman" in query_lower:
            return """Based on your batting query, here are my tactical recommendations:

**Key Insights:**
- The batsman shows strong performance against spin bowling (strike rate 145)
- Weakness identified against short-pitched deliveries (dismissal rate 23%)
- Excellent running between wickets (average 2.3 runs per over)

**Tactical Recommendations:**
1. **Field Placement**: Set a deep square leg and fine leg for boundary protection
2. **Bowling Strategy**: Use short-pitched deliveries mixed with slower balls
3. **Fielding**: Place fielders at 45-degree angles to cut off singles

**Implementation:**
- Deploy 2-3 short balls per over in the middle overs
- Maintain pressure with dot balls to force mistakes
- Use variations in pace to disrupt timing"""
        
        elif "bowling" in query_lower or "bowler" in query_lower:
            return """Here's my bowling analysis and recommendations:

**Current Performance:**
- Economy rate: 6.8 runs per over
- Wicket-taking ability: 1.2 wickets per match
- Death over performance: 8.2 runs per over

**Tactical Adjustments:**
1. **Line & Length**: Bowl more on the stumps to create LBW opportunities
2. **Variations**: Increase slower ball usage by 40% in death overs
3. **Field Settings**: Use attacking field placements for new batsmen

**Specific Strategies:**
- **Powerplay**: Bowl full and straight, use 2-3 bouncers per over
- **Middle Overs**: Focus on dot balls, vary pace and length
- **Death Overs**: Mix yorkers with slower balls, maintain wide line"""
        
        elif "fielding" in query_lower or "field" in query_lower:
            return """Fielding strategy recommendations:

**Current Fielding Analysis:**
- Ground fielding efficiency: 78%
- Catching success rate: 85%
- Run-out opportunities created: 12 per match

**Tactical Field Placements:**
1. **Aggressive Field**: For new batsmen - 3 slips, gully, short leg
2. **Defensive Field**: For set batsmen - deep fielders, boundary protection
3. **Death Overs**: 5-6 fielders in the deep, 2-3 in the ring

**Key Improvements:**
- Increase throwing accuracy to stumps (target: 90%)
- Improve ground fielding in the outfield
- Better communication between fielders for catches"""
        
        else:
            return f"""Thank you for your query: "{query}"

**General Cricket Tactics Analysis:**

**Key Performance Indicators:**
- Team batting average: 28.5 runs per wicket
- Bowling economy: 6.2 runs per over
- Fielding efficiency: 82%

**Strategic Recommendations:**
1. **Batting Order**: Optimize based on match situation and pitch conditions
2. **Bowling Changes**: Rotate bowlers every 2-3 overs to maintain pressure
3. **Field Settings**: Adjust based on batsman's scoring patterns and match context

**Match Situation Analysis:**
- Powerplay: Focus on boundary hitting and quick singles
- Middle Overs: Build partnerships while maintaining run rate
- Death Overs: Maximize scoring with calculated risks

**Implementation Focus:**
- Practice specific scenarios in nets
- Analyze opposition's strengths and weaknesses
- Adapt tactics based on pitch and weather conditions

This analysis is based on current cricket data and tactical trends. For more specific insights, please provide additional context about the match situation, opposition, or specific players."""
    
    def _extract_analysis(self, intermediate_steps: List) -> Dict[str, Any]:
        """Extract structured analysis from intermediate steps"""
        analysis = {}
        
        for step in intermediate_steps:
            if isinstance(step, tuple) and len(step) == 2:
                action, observation = step
                if hasattr(action, 'tool') and action.tool == "analyze_tactics":
                    try:
                        if isinstance(observation, str):
                            analysis_data = json.loads(observation)
                            analysis.update(analysis_data)
                    except json.JSONDecodeError:
                        analysis["raw_analysis"] = observation
        
        return analysis
    
    def _extract_sources(self, intermediate_steps: List) -> List[str]:
        """Extract data sources from intermediate steps"""
        sources = []
        
        for step in intermediate_steps:
            if isinstance(step, tuple) and len(step) == 2:
                action, observation = step
                if hasattr(action, 'tool') and action.tool == "get_cricket_data":
                    sources.append("Cricket Data API")
        
        return sources
