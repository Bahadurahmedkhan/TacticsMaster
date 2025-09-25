"""
Configuration settings for Tactics Master Backend

This module provides centralized configuration management using Pydantic Settings
for type-safe configuration with environment variable support.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    app_name: str = Field(default="Tactics Master API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment (development/production)")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    cors_origins: List[str] = Field(default=["http://localhost:3000"], description="CORS origins")
    
    # LLM settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    gemini_api_key: Optional[str] = Field(default=None, description="Gemini API key")
    default_llm: str = Field(default="gemini", description="Default LLM provider")
    llm_temperature: float = Field(default=0.1, description="LLM temperature")
    llm_max_tokens: int = Field(default=4000, description="LLM max tokens")
    
    # Cricket API settings
    cricket_api_key: Optional[str] = Field(default=None, description="Cricket API key")
    cricapi_key: Optional[str] = Field(default=None, description="CricAPI key")
    espn_cricket_api_key: Optional[str] = Field(default=None, description="ESPN Cricket API key")
    
    # Database settings (if needed in future)
    database_url: Optional[str] = Field(default=None, description="Database URL")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-here", description="Secret key for JWT")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")
    
    # Rate limiting
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    
    # Analysis settings
    max_analysis_timeout: int = Field(default=300, description="Max analysis timeout in seconds")
    max_query_length: int = Field(default=1000, description="Max query length")
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed_envs = ["development", "staging", "production"]
        if v not in allowed_envs:
            raise ValueError(f"Environment must be one of {allowed_envs}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level setting."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v.upper()
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable mapping
        fields = {
            "openai_api_key": {"env": "OPENAI_API_KEY"},
            "gemini_api_key": {"env": "GEMINI_API_KEY"},
            "cricket_api_key": {"env": "CRICKET_API_KEY"},
            "cricapi_key": {"env": "CRICAPI_KEY"},
            "espn_cricket_api_key": {"env": "ESPN_CRICKET_API_KEY"},
            "database_url": {"env": "DATABASE_URL"},
            "secret_key": {"env": "SECRET_KEY"},
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
