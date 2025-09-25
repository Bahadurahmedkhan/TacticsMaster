"""
Tactics Master - Main Application Entry Point

This module serves as the entry point for the Tactics Master agent application.
It loads environment variables, initializes the LLM, and sets up the agent executor
for interactive cricket tactical analysis.

Author: Tactics Master Team
Version: 1.0.0
"""

# Standard library imports
import os
import sys
import logging
from typing import List, Dict, Any, Optional

# Third-party imports
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate

# Local imports
from exceptions import (
    AgentInitializationError, 
    AgentExecutionError, 
    ConfigurationError,
    APIConnectionError,
    APITimeoutError
)

# Import custom tools
from tools.cricket_api_tools import (
    get_player_stats,
    get_team_squad,
    get_matchup_data,
    get_venue_stats
)
from tools.tactical_tools import (
    analyze_weaknesses,
    find_best_matchup,
    generate_bowling_plan,
    generate_fielding_plan
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_environment() -> None:
    """
    Load environment variables from .env file and validate required API keys.
    
    Raises:
        SystemExit: If no valid API keys are found
    """
    try:
        load_dotenv()
        logger.info("Loading environment variables...")
        
        # Check for required environment variables (either OpenAI or Gemini)
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        has_gemini = bool(os.getenv("GEMINI_API_KEY"))
        
        if not has_openai and not has_gemini:
            error_msg = "No API key found. Please set either OPENAI_API_KEY or GEMINI_API_KEY"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            print("Please set these variables in your .env file")
            raise ConfigurationError(
                message=error_msg,
                error_code="MISSING_API_KEY",
                context={"has_openai": has_openai, "has_gemini": has_gemini}
            )
        
        logger.info("Environment variables loaded successfully")
        print("✅ Environment variables loaded successfully")
        
    except ConfigurationError:
        # Re-raise configuration errors
        raise
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
        print(f"❌ Failed to load environment variables: {e}")
        raise ConfigurationError(
            message=f"Failed to load environment variables: {str(e)}",
            error_code="ENV_LOAD_ERROR",
            context={"original_error": str(e)}
        )

def initialize_llm() -> ChatOpenAI | ChatGoogleGenerativeAI:
    """
    Initialize the language model (OpenAI or Gemini).
    
    Returns:
        ChatOpenAI or ChatGoogleGenerativeAI: The initialized language model
        
    Raises:
        SystemExit: If initialization fails or no API keys are found
    """
    try:
        logger.info("Initializing language model...")
        
        # Check for Gemini API key first
        if os.getenv("GEMINI_API_KEY"):
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.1,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
            logger.info("Gemini language model initialized successfully")
            print("✅ Gemini language model initialized successfully")
            return llm
        
        # Fallback to OpenAI
        elif os.getenv("OPENAI_API_KEY"):
            llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("OpenAI language model initialized successfully")
            print("✅ OpenAI language model initialized successfully")
            return llm
        
        else:
            error_msg = "No API key found. Please set either GEMINI_API_KEY or OPENAI_API_KEY"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            raise ConfigurationError(
                message=error_msg,
                error_code="MISSING_API_KEY",
                context={"available_keys": {"openai": bool(os.getenv("OPENAI_API_KEY")), "gemini": bool(os.getenv("GEMINI_API_KEY"))}}
            )
            
    except ConfigurationError:
        # Re-raise configuration errors
        raise
    except Exception as e:
        logger.error(f"Failed to initialize language model: {e}")
        print(f"❌ Failed to initialize language model: {e}")
        raise AgentInitializationError(
            message=f"Failed to initialize language model: {str(e)}",
            error_code="LLM_INIT_ERROR",
            context={"original_error": str(e)}
        )

def create_agent_prompt() -> ChatPromptTemplate:
    """
    Create the agent prompt template.
    
    Returns:
        ChatPromptTemplate: The configured prompt template for the agent
    """
    from langchain.prompts import PromptTemplate
    
    logger.info("Creating agent prompt template...")
    
    return PromptTemplate.from_template("""
You are the Tactics Master, an expert cricket analyst AI that helps coaches make data-driven tactical decisions.

Your role is to:
1. Analyze cricket data (player stats, team info, match history)
2. Identify tactical patterns, weaknesses, and opportunities
3. Provide actionable insights and recommendations for coaches
4. Generate specific bowling and fielding plans

Always structure your analysis with:
- Key findings from the data
- Identified weaknesses or opportunities
- Specific tactical recommendations
- Fielding and bowling strategies

Be concise but comprehensive. Focus on actionable insights that coaches can implement immediately.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}
""")

def _get_available_tools() -> List:
    """
    Get list of available tools for the agent.
    
    Returns:
        List: List of available tools
    """
    return [
        get_player_stats,
        get_team_squad,
        get_matchup_data,
        get_venue_stats,
        analyze_weaknesses,
        find_best_matchup,
        generate_bowling_plan,
        generate_fielding_plan
    ]


def _create_react_agent(llm: ChatOpenAI | ChatGoogleGenerativeAI, tools: List) -> Any:
    """
    Create the ReAct agent with tools and prompt.
    
    Args:
        llm: The language model to use
        tools: List of tools for the agent
        
    Returns:
        ReAct agent instance
    """
    prompt = create_agent_prompt()
    return create_react_agent(llm, tools, prompt)


def _configure_agent_executor(agent: Any, tools: List) -> AgentExecutor:
    """
    Configure and create the agent executor.
    
    Args:
        agent: The ReAct agent instance
        tools: List of tools for the agent
        
    Returns:
        AgentExecutor: Configured agent executor
    """
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=10,
        handle_parsing_errors=True
    )


def create_agent_executor(llm: ChatOpenAI | ChatGoogleGenerativeAI) -> AgentExecutor:
    """
    Create and configure the agent executor.
    
    Args:
        llm: The language model to use for the agent
        
    Returns:
        AgentExecutor: The configured agent executor
        
    Raises:
        AgentInitializationError: If agent creation fails
    """
    try:
        logger.info("Creating agent executor...")
        
        # Get available tools
        tools = _get_available_tools()
        logger.info(f"Loaded {len(tools)} tools for the agent")
        
        # Create the ReAct agent
        agent = _create_react_agent(llm, tools)
        
        # Configure and create the agent executor
        agent_executor = _configure_agent_executor(agent, tools)
        
        logger.info("Agent executor created successfully")
        print("✅ Agent executor created successfully")
        return agent_executor
        
    except Exception as e:
        logger.error(f"Failed to create agent executor: {e}")
        print(f"❌ Failed to create agent executor: {e}")
        raise AgentInitializationError(
            message=f"Failed to create agent executor: {str(e)}",
            error_code="AGENT_CREATION_ERROR",
            context={"original_error": str(e), "tools_count": len(tools)}
        )

def _display_welcome_message() -> None:
    """Display welcome message for the interactive loop."""
    print("\n🏏 Tactics Master Agent is ready!")
    print("Ask me anything about cricket tactics, player analysis, or match strategy.")
    print("Type 'quit' or 'exit' to stop.\n")


def _is_exit_command(user_input: str) -> bool:
    """
    Check if user input is an exit command.
    
    Args:
        user_input: User input string
        
    Returns:
        bool: True if exit command, False otherwise
    """
    return user_input.lower() in ['quit', 'exit', 'q']


def _process_user_query(agent_executor: AgentExecutor, user_input: str) -> None:
    """
    Process a user query through the agent.
    
    Args:
        agent_executor: The configured agent executor
        user_input: User input query
    """
    logger.info(f"Processing user query: {user_input[:50]}...")
    
    # Invoke the agent
    print("\n🤔 Analyzing your request...")
    result = agent_executor.invoke({"input": user_input})
    
    # Display the response
    print(f"\n📊 Tactics Master Analysis:")
    print("=" * 50)
    print(result["output"])
    print("=" * 50)
    
    # Show intermediate steps if verbose
    if result.get("intermediate_steps"):
        steps_count = len(result['intermediate_steps'])
        logger.info(f"Agent used {steps_count} tools")
        print(f"\n🔧 Tools used: {steps_count}")
    
    print("\n" + "-" * 50 + "\n")


def _handle_user_input(agent_executor: AgentExecutor) -> bool:
    """
    Handle user input and return whether to continue the loop.
    
    Args:
        agent_executor: The configured agent executor
        
    Returns:
        bool: True to continue loop, False to exit
    """
    try:
        # Get user input
        user_input = input("Coach: ").strip()
        
        # Check for exit commands
        if _is_exit_command(user_input):
            logger.info("User requested exit")
            print("👋 Goodbye! Thanks for using Tactics Master.")
            return False
        
        # Skip empty inputs
        if not user_input:
            return True
        
        # Process the query
        _process_user_query(agent_executor, user_input)
        return True
        
    except KeyboardInterrupt:
        logger.info("User interrupted with Ctrl+C")
        print("\n👋 Goodbye! Thanks for using Tactics Master.")
        return False
    except AgentExecutionError as e:
        logger.error(f"Agent execution error: {e}")
        print(f"❌ Analysis error: {e.message}")
        print("Please try again or type 'quit' to exit.\n")
        return True
    except Exception as e:
        logger.error(f"Error processing user request: {e}")
        print(f"❌ Error processing your request: {e}")
        print("Please try again or type 'quit' to exit.\n")
        return True


def run_interactive_loop(agent_executor: AgentExecutor) -> None:
    """
    Run the interactive loop for user prompts.
    
    Args:
        agent_executor: The configured agent executor
    """
    _display_welcome_message()
    logger.info("Starting interactive loop")
    
    while True:
        if not _handle_user_input(agent_executor):
            break

def main() -> None:
    """
    Main function to run the Tactics Master agent.
    
    This function orchestrates the initialization and execution of the agent.
    """
    try:
        print("🏏 Starting Tactics Master Agent...")
        logger.info("Starting Tactics Master Agent")
        
        # Load environment variables
        load_environment()
        
        # Initialize the language model
        llm = initialize_llm()
        
        # Create the agent executor
        agent_executor = create_agent_executor(llm)
        
        # Run the interactive loop
        run_interactive_loop(agent_executor)
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n👋 Application stopped by user.")
    except (ConfigurationError, AgentInitializationError) as e:
        logger.error(f"Initialization error: {e}")
        print(f"❌ Initialization error: {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
