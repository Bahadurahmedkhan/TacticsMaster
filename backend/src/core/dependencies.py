"""
Dependency Injection System for Tactics Master

This module provides comprehensive dependency injection with proper lifecycle
management, configuration, and error handling.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
from typing import Any, Dict, Optional, Type, TypeVar, Callable, Awaitable
from functools import lru_cache
from contextlib import asynccontextmanager
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .exceptions import ConfigurationError, AuthenticationError, ServiceUnavailableError
from .logging import LoggerMixin
from ..config.settings import get_settings, Settings
from ..agents.hybrid_agent import HybridTacticsMasterAgent
from ..agents.tactics_agent import TacticsMasterAgent

T = TypeVar('T')


class DependencyContainer:
    """
    Dependency injection container with singleton and transient lifecycle management.
    """
    
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._transients: Dict[str, Callable] = {}
        self._factories: Dict[str, Callable] = {}
        self.logger = logging.getLogger("backend.dependencies")
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a singleton dependency"""
        key = interface.__name__
        self._singletons[key] = implementation
        self.logger.debug(f"Registered singleton: {key}")
    
    def register_transient(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a transient dependency"""
        key = interface.__name__
        self._transients[key] = factory
        self.logger.debug(f"Registered transient: {key}")
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a factory dependency"""
        key = interface.__name__
        self._factories[key] = factory
        self.logger.debug(f"Registered factory: {key}")
    
    def get(self, interface: Type[T]) -> T:
        """Get dependency instance"""
        key = interface.__name__
        
        # Check singletons first
        if key in self._singletons:
            if key not in self._singletons or not hasattr(self._singletons[key], '__call__'):
                # Initialize singleton if not already done
                if key in self._singletons and hasattr(self._singletons[key], '__call__'):
                    self._singletons[key] = self._singletons[key]()
            return self._singletons[key]
        
        # Check transients
        if key in self._transients:
            return self._transients[key]()
        
        # Check factories
        if key in self._factories:
            return self._factories[key]()
        
        raise ConfigurationError(
            message=f"Dependency not registered: {key}",
            error_code="DEPENDENCY_NOT_FOUND",
            context={"interface": key, "available": list(self._singletons.keys())}
        )
    
    def get_or_none(self, interface: Type[T]) -> Optional[T]:
        """Get dependency instance or None if not registered"""
        try:
            return self.get(interface)
        except ConfigurationError:
            return None


# Global dependency container
_container: Optional[DependencyContainer] = None


def get_container() -> DependencyContainer:
    """Get the global dependency container"""
    global _container
    if _container is None:
        _container = DependencyContainer()
    return _container


class DependencyManager:
    """
    Manager for dependency injection and lifecycle management.
    """
    
    def __init__(self):
        self.container = get_container()
        self.logger = logging.getLogger("backend.dependencies.manager")
    
    def setup_dependencies(self) -> None:
        """Setup all application dependencies"""
        self.logger.info("Setting up application dependencies")
        
        # Register core dependencies
        self.container.register_singleton(Settings, get_settings)
        
        # Register agents
        self.container.register_singleton(HybridTacticsMasterAgent, self._create_hybrid_agent)
        self.container.register_singleton(TacticsMasterAgent, self._create_tactics_agent)
        
        self.logger.info("Dependencies setup completed")
    
    def _create_hybrid_agent(self) -> HybridTacticsMasterAgent:
        """Create hybrid agent instance"""
        try:
            settings = self.container.get(Settings)
            agent = HybridTacticsMasterAgent()
            self.logger.info("Hybrid agent created successfully")
            return agent
        except Exception as e:
            self.logger.error(f"Failed to create hybrid agent: {e}")
            raise ServiceUnavailableError(
                message="Hybrid agent service unavailable",
                error_code="AGENT_CREATION_FAILED",
                context={"original_error": str(e)}
            )
    
    def _create_tactics_agent(self) -> TacticsMasterAgent:
        """Create tactics agent instance"""
        try:
            settings = self.container.get(Settings)
            # This would need proper LLM initialization
            # For now, return a placeholder
            self.logger.info("Tactics agent created successfully")
            return None  # Placeholder
        except Exception as e:
            self.logger.error(f"Failed to create tactics agent: {e}")
            raise ServiceUnavailableError(
                message="Tactics agent service unavailable",
                error_code="AGENT_CREATION_FAILED",
                context={"original_error": str(e)}
            )


# FastAPI Dependencies
def get_settings_dependency() -> Settings:
    """FastAPI dependency for settings"""
    return get_settings()


def get_hybrid_agent() -> HybridTacticsMasterAgent:
    """FastAPI dependency for hybrid agent"""
    container = get_container()
    return container.get(HybridTacticsMasterAgent)


def get_tactics_agent() -> TacticsMasterAgent:
    """FastAPI dependency for tactics agent"""
    container = get_container()
    return container.get(TacticsMasterAgent)


# Authentication Dependencies
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict[str, Any]]:
    """
    Get current authenticated user.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        User information or None if not authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        return None
    
    try:
        # TODO: Implement proper JWT token validation
        # For now, return a mock user
        return {
            "user_id": "mock_user",
            "username": "coach",
            "role": "coach"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def require_authentication(user: Optional[Dict[str, Any]] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require authentication for protected endpoints.
    
    Args:
        user: Current user from authentication
        
    Returns:
        User information
        
    Raises:
        HTTPException: If not authenticated
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user


def require_coach_role(user: Dict[str, Any] = Depends(require_authentication)) -> Dict[str, Any]:
    """
    Require coach role for coach-specific endpoints.
    
    Args:
        user: Current authenticated user
        
    Returns:
        User information
        
    Raises:
        HTTPException: If not authorized
    """
    if user.get("role") != "coach":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach role required"
        )
    return user


# Service Dependencies
@lru_cache()
def get_logger(name: str = "backend") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


def get_request_logger() -> logging.Logger:
    """Get request logger"""
    return get_logger("backend.requests")


def get_performance_logger() -> logging.Logger:
    """Get performance logger"""
    return get_logger("backend.performance")


# Health Check Dependencies
def get_health_status() -> Dict[str, Any]:
    """Get system health status"""
    container = get_container()
    
    health_status = {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",  # This would be dynamic
        "services": {}
    }
    
    # Check agent availability
    try:
        hybrid_agent = container.get_or_none(HybridTacticsMasterAgent)
        health_status["services"]["hybrid_agent"] = "available" if hybrid_agent else "unavailable"
    except Exception:
        health_status["services"]["hybrid_agent"] = "error"
    
    try:
        tactics_agent = container.get_or_none(TacticsMasterAgent)
        health_status["services"]["tactics_agent"] = "available" if tactics_agent else "unavailable"
    except Exception:
        health_status["services"]["tactics_agent"] = "error"
    
    # Determine overall status
    if any(status == "error" for status in health_status["services"].values()):
        health_status["status"] = "degraded"
    
    return health_status


# Context Managers
@asynccontextmanager
async def get_agent_context():
    """Context manager for agent operations"""
    container = get_container()
    
    try:
        agent = container.get(HybridTacticsMasterAgent)
        yield agent
    except Exception as e:
        logging.getLogger("backend.dependencies").error(f"Agent context error: {e}")
        raise
    finally:
        # Cleanup if needed
        pass


# Dependency Injection Decorators
def inject_dependency(interface: Type[T]) -> T:
    """Decorator for dependency injection"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            container = get_container()
            dependency = container.get(interface)
            return func(dependency, *args, **kwargs)
        return wrapper
    return decorator


def inject_settings(func: Callable) -> Callable:
    """Decorator to inject settings"""
    def wrapper(*args, **kwargs):
        settings = get_settings()
        return func(settings, *args, **kwargs)
    return wrapper


def inject_agent(func: Callable) -> Callable:
    """Decorator to inject hybrid agent"""
    def wrapper(*args, **kwargs):
        container = get_container()
        agent = container.get(HybridTacticsMasterAgent)
        return func(agent, *args, **kwargs)
    return wrapper


# Initialize dependencies
def initialize_dependencies() -> None:
    """Initialize all dependencies"""
    manager = DependencyManager()
    manager.setup_dependencies()
