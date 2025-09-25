"""
Tactics Master Agent - Core Agent Logic

This module contains the core agent definition and logic for the Tactics Master.
It defines the agent's prompt template and provides methods for creating
and configuring the LangChain agent.

Author: Tactics Master Team
Version: 1.0.0
"""

# Standard library imports
import logging
from typing import List, Dict, Any, Optional, Union

# Third-party imports
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Local imports
from exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ToolExecutionError,
    ValidationError
)

# Configure logging
logger = logging.getLogger(__name__)

class TacticsMasterAgent:
    """
    The Tactics Master agent for cricket tactical analysis.
    
    This agent is designed to help coaches make data-driven tactical decisions
    by analyzing cricket data and providing actionable insights.
    
    Attributes:
        llm: The language model instance
        tools: List of available tools
        verbose: Verbose logging flag
        agent_executor: The configured agent executor
    """
    
    def __init__(
        self, 
        llm: Union[ChatGoogleGenerativeAI, ChatOpenAI], 
        tools: List, 
        verbose: bool = True
    ) -> None:
        """
        Initialize the Tactics Master agent.
        
        Args:
            llm: The language model to use
            tools: List of tools available to the agent
            verbose: Whether to enable verbose logging
            
        Raises:
            ValueError: If llm or tools are None or empty
        """
        if not llm:
            raise AgentInitializationError(
                message="Language model cannot be None",
                error_code="INVALID_LLM",
                context={"llm_type": type(llm).__name__}
            )
        if not tools:
            raise AgentInitializationError(
                message="Tools list cannot be empty",
                error_code="EMPTY_TOOLS_LIST",
                context={"tools_count": len(tools) if tools else 0}
            )
            
        self.llm = llm
        self.tools = tools
        self.verbose = verbose
        self.agent_executor: Optional[AgentExecutor] = None
        
        logger.info(f"Initialized TacticsMasterAgent with {len(tools)} tools")
        
    def create_agent_prompt(self) -> ChatPromptTemplate:
        """
        Create the agent prompt template.
        
        Returns:
            ChatPromptTemplate: The configured prompt template
        """
        logger.info("Creating agent prompt template")
        return ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the agent.
        
        Returns:
            str: The system prompt text
        """
        return """
You are the Tactics Master, an expert cricket analyst AI that helps coaches make data-driven tactical decisions.

Your role is to:
1. Analyze cricket data (player stats, team info, match history)
2. Identify tactical patterns, weaknesses, and opportunities
3. Provide actionable insights and recommendations for coaches
4. Generate specific bowling and fielding plans

Available tools:
- get_player_stats: Fetch detailed player statistics and recent form
- get_team_squad: Get team squad information and player roles
- get_matchup_data: Retrieve head-to-head records and historical data
- get_venue_stats: Get venue-specific statistics and conditions
- analyze_weaknesses: Analyze player vulnerabilities and patterns
- find_best_matchup: Identify optimal player vs player matchups
- generate_bowling_plan: Create specific bowling strategies
- generate_fielding_plan: Design fielding setups and positions

Always structure your analysis with:
- Key findings from the data
- Identified weaknesses or opportunities
- Specific tactical recommendations
- Fielding and bowling strategies

Be concise but comprehensive. Focus on actionable insights that coaches can implement immediately.
        """
    
    def create_agent(self) -> AgentExecutor:
        """
        Create the agent executor.
        
        Returns:
            AgentExecutor: The configured agent executor
            
        Raises:
            Exception: If agent creation fails
        """
        try:
            logger.info("Creating agent executor")
            
            # Create the agent prompt
            prompt = self.create_agent_prompt()
            
            # Create the ReAct agent
            agent = create_react_agent(self.llm, self.tools, prompt)
            
            # Create the agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=self.verbose,
                return_intermediate_steps=True,
                max_iterations=10,
                handle_parsing_errors=True
            )
            
            logger.info("Agent executor created successfully")
            return self.agent_executor
            
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise AgentInitializationError(
                message=f"Failed to create agent: {str(e)}",
                error_code="AGENT_CREATION_FAILED",
                context={"original_error": str(e), "tools_count": len(self.tools)}
            )
    
    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a cricket tactics query.
        
        Args:
            query: The coach's question or request
            context: Additional context (team, opponent, etc.)
            
        Returns:
            Dict[str, Any]: Analysis results containing:
                - response: The analysis response
                - intermediate_steps: Steps taken by the agent
                - success: Whether the analysis was successful
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            raise ValidationError(
                message="Query cannot be empty",
                error_code="EMPTY_QUERY",
                context={"query_length": len(query) if query else 0}
            )
        
        if not self.agent_executor:
            logger.info("Agent executor not initialized, creating now")
            self.create_agent()
        
        try:
            logger.info(f"Analyzing query: {query[:50]}...")
            
            # Prepare input for the agent
            agent_input = {
                "input": query,
                "context": context or {}
            }
            
            # Run the agent
            result = self.agent_executor.invoke(agent_input)
            
            logger.info("Analysis completed successfully")
            return {
                "response": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
                "success": True
            }
            
        except ValidationError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise AgentExecutionError(
                message=f"Analysis failed: {str(e)}",
                error_code="ANALYSIS_EXECUTION_ERROR",
                context={"query": query[:50], "original_error": str(e)}
            )
    
    def get_available_tools(self) -> List[str]:
        """
        Get list of available tool names.
        
        Returns:
            List[str]: List of tool names
        """
        try:
            return [tool.name for tool in self.tools]
        except Exception as e:
            logger.error(f"Error getting tool names: {e}")
            return []
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.
        
        Returns:
            Dict[str, Any]: Agent information containing:
                - name: Agent name
                - version: Agent version
                - description: Agent description
                - available_tools: List of available tools
                - model: Language model name
        """
        try:
            model_name = "Unknown"
            if hasattr(self.llm, 'model_name'):
                model_name = self.llm.model_name
            elif hasattr(self.llm, 'model'):
                model_name = self.llm.model
            
            return {
                "name": "Tactics Master",
                "version": "1.0.0",
                "description": "AI-powered cricket tactical analysis agent",
                "available_tools": self.get_available_tools(),
                "model": model_name,
                "tools_count": len(self.tools),
                "verbose": self.verbose
            }
        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return {
                "name": "Tactics Master",
                "version": "1.0.0",
                "description": "AI-powered cricket tactical analysis agent",
                "available_tools": [],
                "model": "Unknown",
                "tools_count": 0,
                "verbose": False
            }
