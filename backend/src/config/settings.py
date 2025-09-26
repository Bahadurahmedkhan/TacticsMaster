"""
Enhanced Configuration Management for Tactics Master System

This module provides comprehensive configuration management with environment-specific
settings, validation, and secure handling of sensitive data.

Author: Tactics Master Team
Version: 2.0.0
"""

import os
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from enum import Enum
from pydantic import BaseSettings, Field, validator, root_validator
from pydantic.env_settings import SettingsSourceCallable

from ..core.exceptions import ConfigurationError


class Environment(str, Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    
    url: str = Field(..., description="Database connection URL")
    pool_size: int = Field(default=10, ge=1, le=100, description="Connection pool size")
    max_overflow: int = Field(default=20, ge=0, le=100, description="Maximum overflow connections")
    pool_timeout: int = Field(default=30, ge=1, le=300, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=3600, ge=300, le=7200, description="Pool recycle time in seconds")
    echo: bool = Field(default=False, description="Enable SQL query logging")
    
    class Config:
        env_prefix = "DB_"


class APISettings(BaseSettings):
    """API configuration"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="OpenAI temperature")
    openai_max_tokens: int = Field(default=4000, ge=1, le=8000, description="Maximum tokens for OpenAI")
    
    # Gemini Configuration
    gemini_api_key: Optional[str] = Field(default=None, description="Gemini API key")
    gemini_model: str = Field(default="gemini-1.5-flash", description="Gemini model to use")
    gemini_temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Gemini temperature")
    
    # Cricket API Configuration
    cricket_api_key: Optional[str] = Field(default=None, description="Cricket API key")
    cricapi_key: Optional[str] = Field(default=None, description="CricAPI key")
    espn_cricket_api_key: Optional[str] = Field(default=None, description="ESPN Cricket API key")
    
    # API Rate Limiting
    rate_limit_requests: int = Field(default=100, ge=1, le=10000, description="Rate limit requests per minute")
    rate_limit_window: int = Field(default=60, ge=1, le=3600, description="Rate limit window in seconds")
    
    # API Timeouts
    request_timeout: int = Field(default=30, ge=1, le=300, description="Request timeout in seconds")
    connection_timeout: int = Field(default=10, ge=1, le=60, description="Connection timeout in seconds")
    
    class Config:
        env_prefix = "API_"


class SecuritySettings(BaseSettings):
    """Security configuration"""
    
    secret_key: str = Field(..., description="Secret key for JWT tokens")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440, description="Access token expiry in minutes")
    refresh_token_expire_days: int = Field(default=7, ge=1, le=30, description="Refresh token expiry in days")
    
    # CORS Settings
    cors_origins: List[str] = Field(default=["http://localhost:3000"], description="CORS allowed origins")
    cors_methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE"], description="CORS allowed methods")
    cors_headers: List[str] = Field(default=["*"], description="CORS allowed headers")
    
    # Security Headers
    enable_security_headers: bool = Field(default=True, description="Enable security headers")
    content_security_policy: str = Field(
        default="default-src 'self'",
        description="Content Security Policy"
    )
    
    class Config:
        env_prefix = "SECURITY_"


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    
    level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    format: str = Field(default="json", description="Log format (json or text)")
    file_path: Optional[str] = Field(default=None, description="Log file path")
    max_file_size: int = Field(default=10485760, ge=1024, le=104857600, description="Max log file size in bytes")
    backup_count: int = Field(default=5, ge=1, le=20, description="Number of backup log files")
    enable_performance_logging: bool = Field(default=True, description="Enable performance logging")
    enable_request_logging: bool = Field(default=True, description="Enable request logging")
    
    class Config:
        env_prefix = "LOG_"


class CacheSettings(BaseSettings):
    """Cache configuration"""
    
    enabled: bool = Field(default=True, description="Enable caching")
    backend: str = Field(default="memory", description="Cache backend (memory, redis)")
    redis_url: Optional[str] = Field(default=None, description="Redis URL for cache")
    default_ttl: int = Field(default=300, ge=1, le=3600, description="Default TTL in seconds")
    max_size: int = Field(default=1000, ge=10, le=10000, description="Maximum cache size")
    
    class Config:
        env_prefix = "CACHE_"


class Settings(BaseSettings):
    """Main application settings"""
    
    # Environment
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Application
    app_name: str = Field(default="Tactics Master", description="Application name")
    app_version: str = Field(default="2.0.0", description="Application version")
    app_description: str = Field(
        default="AI-powered cricket tactical analysis platform",
        description="Application description"
    )
    
    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    workers: int = Field(default=1, ge=1, le=32, description="Number of worker processes")
    
    # Database
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # APIs
    api: APISettings = Field(default_factory=APISettings)
    
    # Security
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    
    # Logging
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    # Cache
    cache: CacheSettings = Field(default_factory=CacheSettings)
    
    # Feature Flags
    enable_ai_analysis: bool = Field(default=True, description="Enable AI analysis features")
    enable_real_data: bool = Field(default=True, description="Enable real cricket data")
    enable_caching: bool = Field(default=True, description="Enable response caching")
    enable_metrics: bool = Field(default=True, description="Enable performance metrics")
    
    # Performance
    max_request_size: int = Field(default=10485760, ge=1024, le=104857600, description="Max request size in bytes")
    request_timeout: int = Field(default=300, ge=1, le=1800, description="Request timeout in seconds")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting"""
        if v not in [e.value for e in Environment]:
            raise ValueError(f"Invalid environment: {v}")
        return v
    
    @validator("debug")
    def validate_debug(cls, v, values):
        """Validate debug setting based on environment"""
        environment = values.get("environment", Environment.DEVELOPMENT)
        if environment == Environment.PRODUCTION and v:
            raise ValueError("Debug mode cannot be enabled in production")
        return v
    
    @root_validator
    def validate_api_keys(cls, values):
        """Validate that at least one AI API key is provided"""
        api_settings = values.get("api", {})
        
        if not any([
            api_settings.get("openai_api_key"),
            api_settings.get("gemini_api_key")
        ]):
            raise ValueError("At least one AI API key (OpenAI or Gemini) must be provided")
        
        return values
    
    @root_validator
    def validate_security_settings(cls, values):
        """Validate security settings"""
        security = values.get("security", {})
        environment = values.get("environment", Environment.DEVELOPMENT)
        
        # In production, require strong security settings
        if environment == Environment.PRODUCTION:
            if not security.get("secret_key") or len(security.get("secret_key", "")) < 32:
                raise ValueError("Secret key must be at least 32 characters in production")
            
            if security.get("access_token_expire_minutes", 0) > 60:
                raise ValueError("Access token expiry should not exceed 60 minutes in production")
        
        return values
    
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        return self.database.url
    
    def get_ai_provider(self) -> str:
        """Get the preferred AI provider based on available keys"""
        if self.api.openai_api_key:
            return "openai"
        elif self.api.gemini_api_key:
            return "gemini"
        else:
            raise ConfigurationError(
                message="No AI provider available",
                error_code="NO_AI_PROVIDER",
                context={"available_keys": {
                    "openai": bool(self.api.openai_api_key),
                    "gemini": bool(self.api.gemini_api_key)
                }}
            )
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == Environment.PRODUCTION
    
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.environment == Environment.TESTING
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        if self.is_development():
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        elif self.is_production():
            return self.security.cors_origins
        else:
            return ["*"]
    
    def get_log_level(self) -> str:
        """Get appropriate log level based on environment"""
        if self.is_development():
            return "DEBUG"
        elif self.is_production():
            return "WARNING"
        else:
            return self.logging.level.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary (excluding sensitive data)"""
        settings_dict = self.dict()
        
        # Remove sensitive data
        sensitive_keys = [
            "api.openai_api_key",
            "api.gemini_api_key",
            "api.cricket_api_key",
            "api.cricapi_key",
            "api.espn_cricket_api_key",
            "security.secret_key"
        ]
        
        for key in sensitive_keys:
            keys = key.split(".")
            current = settings_dict
            for k in keys[:-1]:
                current = current[k]
            if keys[-1] in current:
                current[keys[-1]] = "***REDACTED***"
        
        return settings_dict


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings (singleton pattern).
    
    Returns:
        Settings: Application settings instance
    """
    global _settings
    
    if _settings is None:
        try:
            _settings = Settings()
        except Exception as e:
            raise ConfigurationError(
                message=f"Failed to load configuration: {str(e)}",
                error_code="CONFIG_LOAD_ERROR",
                context={"original_error": str(e)}
            )
    
    return _settings


def reload_settings() -> Settings:
    """
    Reload application settings.
    
    Returns:
        Settings: Reloaded settings instance
    """
    global _settings
    _settings = None
    return get_settings()


# Environment-specific settings
def get_development_settings() -> Settings:
    """Get development-specific settings"""
    return Settings(
        environment=Environment.DEVELOPMENT,
        debug=True,
        logging=LoggingSettings(level=LogLevel.DEBUG),
        database=DatabaseSettings(echo=True)
    )


def get_production_settings() -> Settings:
    """Get production-specific settings"""
    return Settings(
        environment=Environment.PRODUCTION,
        debug=False,
        logging=LoggingSettings(level=LogLevel.WARNING),
        database=DatabaseSettings(echo=False)
    )


def get_testing_settings() -> Settings:
    """Get testing-specific settings"""
    return Settings(
        environment=Environment.TESTING,
        debug=True,
        logging=LoggingSettings(level=LogLevel.DEBUG),
        database=DatabaseSettings(echo=False)
    )