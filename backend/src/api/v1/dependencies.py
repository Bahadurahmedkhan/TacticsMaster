"""
API Dependencies for Tactics Master

This module provides FastAPI dependencies for authentication,
authorization, and service access.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ...core.dependencies import (
    get_hybrid_agent,
    get_current_user,
    require_authentication,
    get_health_status
)

# Configure logging
logger = logging.getLogger("backend.api.dependencies")

# Security scheme
security = HTTPBearer(auto_error=False)


def get_hybrid_agent_dependency():
    """Get hybrid agent dependency"""
    try:
        from ...core.dependencies import get_container
        container = get_container()
        return container.get("HybridTacticsMasterAgent")
    except Exception as e:
        logger.error(f"Failed to get hybrid agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analysis service unavailable"
        )


def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict[str, Any]]:
    """Get current user dependency"""
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
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def require_authentication_dependency(user: Optional[Dict[str, Any]] = Depends(get_current_user_dependency)) -> Dict[str, Any]:
    """Require authentication dependency"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user


def require_coach_role_dependency(user: Dict[str, Any] = Depends(require_authentication_dependency)) -> Dict[str, Any]:
    """Require coach role dependency"""
    if user.get("role") != "coach":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach role required"
        )
    return user


async def get_health_status_dependency() -> Dict[str, Any]:
    """Get health status dependency"""
    try:
        return await get_health_status()
    except Exception as e:
        logger.error(f"Health status check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-01T12:00:00Z"
        }
