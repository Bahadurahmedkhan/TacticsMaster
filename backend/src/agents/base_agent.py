"""
Base Agent Class for Tactics Master System

This module provides the foundational agent class with comprehensive error handling,
logging, and lifecycle management for all specialized agents.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Type
from datetime import datetime
from enum import Enum

from ..core.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ValidationError,
    TacticsMasterError
)
from ..core.logging import LoggerMixin, PerformanceLogger
from ..core.validation import Validator


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class AgentCapability(str, Enum):
    """Agent capability enumeration"""
    DATA_ANALYSIS = "data_analysis"
    TACTICAL_PLANNING = "tactical_planning"
    PLAYER_ANALYSIS = "player_analysis"
    TEAM_ANALYSIS = "team_analysis"
    MATCHUP_ANALYSIS = "matchup_analysis"
    VENUE_ANALYSIS = "venue_analysis"


class BaseAgent(ABC, LoggerMixin):
    """
    Base class for all Tactics Master agents.
    
    Provides common functionality including error handling, logging,
    performance monitoring, and lifecycle management.
    """
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        capabilities: Optional[List[AgentCapability]] = None,
        max_concurrent_requests: int = 10,
        request_timeout: int = 300
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            version: Agent version
            capabilities: List of agent capabilities
            max_concurrent_requests: Maximum concurrent requests
            request_timeout: Request timeout in seconds
        """
        self.name = name
        self.version = version
        self.capabilities = capabilities or []
        self.max_concurrent_requests = max_concurrent_requests
        self.request_timeout = request_timeout
        
        # State management
        self._status = AgentStatus.INITIALIZING
        self._active_requests = 0
        self._performance_logger = PerformanceLogger()
        self._initialization_time = None
        self._last_activity = None
        
        # Error tracking
        self._error_count = 0
        self._last_error = None
        
        self.logger.info(f"Initializing {self.name} agent v{self.version}")
    
    @property
    def status(self) -> AgentStatus:
        """Get current agent status"""
        return self._status
    
    @property
    def is_ready(self) -> bool:
        """Check if agent is ready to process requests"""
        return self._status == AgentStatus.READY
    
    @property
    def is_busy(self) -> bool:
        """Check if agent is currently busy"""
        return self._status == AgentStatus.BUSY
    
    @property
    def active_requests(self) -> int:
        """Get number of active requests"""
        return self._active_requests
    
    @property
    def error_count(self) -> int:
        """Get total error count"""
        return self._error_count
    
    @property
    def uptime(self) -> float:
        """Get agent uptime in seconds"""
        if self._initialization_time is None:
            return 0.0
        return (datetime.now() - self._initialization_time).total_seconds()
    
    async def initialize(self) -> None:
        """
        Initialize the agent.
        
        Raises:
            AgentInitializationError: If initialization fails
        """
        try:
            self.logger.info(f"Starting initialization of {self.name} agent")
            self._status = AgentStatus.INITIALIZING
            
            # Perform agent-specific initialization
            await self._initialize_agent()
            
            self._status = AgentStatus.READY
            self._initialization_time = datetime.now()
            self.logger.info(f"{self.name} agent initialized successfully")
            
        except Exception as e:
            self._status = AgentStatus.ERROR
            self._last_error = e
            self.logger.error(f"Failed to initialize {self.name} agent: {e}")
            raise AgentInitializationError(
                message=f"Agent initialization failed: {str(e)}",
                error_code="AGENT_INIT_FAILED",
                context={"agent_name": self.name, "original_error": str(e)}
            )
    
    @abstractmethod
    async def _initialize_agent(self) -> None:
        """Agent-specific initialization logic"""
        pass
    
    async def analyze(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze a cricket tactics query.
        
        Args:
            query: The analysis query
            context: Additional context
            **kwargs: Additional parameters
            
        Returns:
            Analysis results
            
        Raises:
            AgentExecutionError: If analysis fails
            ValidationError: If input validation fails
        """
        if not self.is_ready:
            raise AgentExecutionError(
                message="Agent is not ready",
                error_code="AGENT_NOT_READY",
                context={"agent_status": self._status.value}
            )
        
        if self._active_requests >= self.max_concurrent_requests:
            raise AgentExecutionError(
                message="Agent is at maximum capacity",
                error_code="AGENT_OVERLOADED",
                context={"active_requests": self._active_requests, "max_requests": self.max_concurrent_requests}
            )
        
        # Validate input
        validated_query = self._validate_query(query)
        validated_context = self._validate_context(context or {})
        
        # Track request
        self._active_requests += 1
        self._status = AgentStatus.BUSY
        self._last_activity = datetime.now()
        
        operation_id = f"{self.name}_analysis_{datetime.now().timestamp()}"
        self._performance_logger.start_timer(operation_id)
        
        try:
            # Perform analysis
            result = await self._perform_analysis(validated_query, validated_context, **kwargs)
            
            # Log performance
            duration = self._performance_logger.end_timer(operation_id)
            self.logger.info(f"Analysis completed in {duration:.3f}s")
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._last_error = e
            self.logger.error(f"Analysis failed: {e}")
            raise AgentExecutionError(
                message=f"Analysis failed: {str(e)}",
                error_code="ANALYSIS_FAILED",
                context={"query": query[:100], "original_error": str(e)}
            )
        
        finally:
            self._active_requests -= 1
            if self._active_requests == 0:
                self._status = AgentStatus.READY
    
    @abstractmethod
    async def _perform_analysis(
        self,
        query: str,
        context: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Agent-specific analysis logic"""
        pass
    
    def _validate_query(self, query: str) -> str:
        """Validate analysis query"""
        if not query or not query.strip():
            raise ValidationError(
                message="Query cannot be empty",
                error_code="EMPTY_QUERY",
                context={"query_length": len(query) if query else 0}
            )
        
        validated_query = Validator.validate_string(
            value=query,
            required=True,
            min_length=1,
            max_length=2000,
            field_name="query"
        )
        
        return validated_query
    
    def _validate_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate analysis context"""
        if not isinstance(context, dict):
            raise ValidationError(
                message="Context must be a dictionary",
                error_code="INVALID_CONTEXT_TYPE",
                context={"context_type": type(context).__name__}
            )
        
        # Validate context size
        if len(str(context)) > 10000:  # 10KB limit
            raise ValidationError(
                message="Context too large",
                error_code="CONTEXT_TOO_LARGE",
                context={"context_size": len(str(context))}
            )
        
        return context
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities"""
        return self.capabilities.copy()
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get comprehensive status information"""
        return {
            "name": self.name,
            "version": self.version,
            "status": self._status.value,
            "capabilities": [cap.value for cap in self.capabilities],
            "active_requests": self._active_requests,
            "max_concurrent_requests": self.max_concurrent_requests,
            "error_count": self._error_count,
            "uptime_seconds": self.uptime,
            "last_activity": self._last_activity.isoformat() if self._last_activity else None,
            "last_error": str(self._last_error) if self._last_error else None,
            "initialization_time": self._initialization_time.isoformat() if self._initialization_time else None
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        health_status = {
            "healthy": self.is_ready and self._error_count < 10,
            "status": self._status.value,
            "uptime": self.uptime,
            "error_count": self._error_count,
            "active_requests": self._active_requests,
            "capabilities": [cap.value for cap in self.capabilities]
        }
        
        if self._last_error:
            health_status["last_error"] = str(self._last_error)
        
        return health_status
    
    async def shutdown(self) -> None:
        """Shutdown the agent gracefully"""
        self.logger.info(f"Shutting down {self.name} agent")
        self._status = AgentStatus.SHUTDOWN
        
        # Wait for active requests to complete
        timeout = 30  # 30 seconds timeout
        start_time = datetime.now()
        
        while self._active_requests > 0:
            if (datetime.now() - start_time).total_seconds() > timeout:
                self.logger.warning(f"Timeout waiting for {self._active_requests} active requests to complete")
                break
            await asyncio.sleep(0.1)
        
        self.logger.info(f"{self.name} agent shutdown completed")
    
    def __str__(self) -> str:
        return f"{self.name} Agent v{self.version} ({self._status.value})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', status='{self._status.value}')>"
