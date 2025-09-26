"""
Enhanced Logging Configuration for Tactics Master System

This module provides comprehensive logging setup with structured logging,
performance monitoring, and proper log formatting for production environments.

Author: Tactics Master Team
Version: 2.0.0
"""

import logging
import logging.config
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter for structured JSON logging.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "process": record.process
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in log_entry and not key.startswith('_'):
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


class PerformanceFilter(logging.Filter):
    """
    Filter to add performance metrics to log records.
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add performance metrics to log record"""
        # Add memory usage if available
        try:
            import psutil
            process = psutil.Process()
            record.memory_mb = round(process.memory_info().rss / 1024 / 1024, 2)
            record.cpu_percent = round(process.cpu_percent(), 2)
        except ImportError:
            record.memory_mb = None
            record.cpu_percent = None
        
        return True


class LoggingConfig:
    """
    Centralized logging configuration for the Tactics Master system.
    """
    
    @staticmethod
    def get_logging_config(
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        enable_structured: bool = True,
        enable_performance: bool = True
    ) -> Dict[str, Any]:
        """
        Get logging configuration dictionary.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            enable_structured: Enable structured JSON logging
            enable_performance: Enable performance metrics
            
        Returns:
            Dict containing logging configuration
        """
        handlers = {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "structured" if enable_structured else "standard",
                "stream": "ext://sys.stdout"
            }
        }
        
        if log_file:
            handlers["file"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "structured" if enable_structured else "standard",
                "filename": log_file,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        
        formatters = {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "structured": {
                "()": "backend.src.core.logging.StructuredFormatter"
            }
        }
        
        filters = {}
        if enable_performance:
            filters["performance"] = {
                "()": "backend.src.core.logging.PerformanceFilter"
            }
        
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": formatters,
            "filters": filters,
            "handlers": handlers,
            "loggers": {
                "": {  # Root logger
                    "level": log_level,
                    "handlers": list(handlers.keys()),
                    "filters": ["performance"] if enable_performance else []
                },
                "backend": {
                    "level": log_level,
                    "handlers": list(handlers.keys()),
                    "filters": ["performance"] if enable_performance else [],
                    "propagate": False
                },
                "uvicorn": {
                    "level": "INFO",
                    "handlers": list(handlers.keys()),
                    "propagate": False
                },
                "fastapi": {
                    "level": "INFO",
                    "handlers": list(handlers.keys()),
                    "propagate": False
                }
            }
        }
    
    @staticmethod
    def setup_logging(
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        enable_structured: bool = True,
        enable_performance: bool = True
    ) -> None:
        """
        Setup logging configuration.
        
        Args:
            log_level: Logging level
            log_file: Optional log file path
            enable_structured: Enable structured JSON logging
            enable_performance: Enable performance metrics
        """
        config = LoggingConfig.get_logging_config(
            log_level=log_level,
            log_file=log_file,
            enable_structured=enable_structured,
            enable_performance=enable_performance
        )
        
        logging.config.dictConfig(config)
        
        # Set up specific loggers
        logger = logging.getLogger("backend")
        logger.info("Logging configuration initialized")


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for the current class"""
        return logging.getLogger(f"backend.{self.__class__.__module__}.{self.__class__.__name__}")


class PerformanceLogger:
    """
    Utility class for performance logging and monitoring.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("backend.performance")
        self._start_times: Dict[str, float] = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        import time
        self._start_times[operation] = time.time()
        self.logger.debug(f"Started timing operation: {operation}")
    
    def end_timer(self, operation: str, log_level: int = logging.INFO) -> float:
        """
        End timing an operation and log the duration.
        
        Args:
            operation: Operation name
            log_level: Log level for the timing message
            
        Returns:
            Duration in seconds
        """
        import time
        
        if operation not in self._start_times:
            self.logger.warning(f"No start time found for operation: {operation}")
            return 0.0
        
        duration = time.time() - self._start_times[operation]
        del self._start_times[operation]
        
        self.logger.log(log_level, f"Operation '{operation}' completed in {duration:.3f}s")
        return duration
    
    def log_performance_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log performance metrics"""
        self.logger.info(f"Performance metrics: {json.dumps(metrics, default=str)}")


class RequestLogger:
    """
    Logger for HTTP requests and responses.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("backend.requests")
    
    def log_request(
        self,
        method: str,
        url: str,
        status_code: int,
        duration: float,
        user_id: Optional[str] = None,
        **kwargs
    ) -> None:
        """Log HTTP request details"""
        log_data = {
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_id": user_id,
            **kwargs
        }
        
        if status_code >= 400:
            self.logger.warning(f"HTTP Request: {json.dumps(log_data)}")
        else:
            self.logger.info(f"HTTP Request: {json.dumps(log_data)}")


# Initialize default logging
def initialize_logging() -> None:
    """Initialize default logging configuration"""
    LoggingConfig.setup_logging(
        log_level="INFO",
        enable_structured=True,
        enable_performance=True
    )
