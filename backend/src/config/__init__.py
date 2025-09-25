"""
Configuration package for Tactics Master Backend

This package contains configuration management utilities including
settings, database configuration, and environment-specific configs.
"""

from .settings import Settings, get_settings, settings

__all__ = ["Settings", "get_settings", "settings"]
