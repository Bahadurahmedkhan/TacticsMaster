"""
Comprehensive Input Validation System for Tactics Master

This module provides robust input validation with detailed error messages,
type checking, and data sanitization for all API endpoints and internal functions.

Author: Tactics Master Team
Version: 2.0.0
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Type, get_type_hints
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, ValidationError as PydanticValidationError
from pydantic.validators import str_validator

from .exceptions import ValidationError, DataValidationError


class ValidationRule:
    """Base class for validation rules"""
    
    def __init__(self, error_message: str):
        self.error_message = error_message
    
    def validate(self, value: Any) -> bool:
        """Validate the value"""
        raise NotImplementedError


class RequiredRule(ValidationRule):
    """Rule for required fields"""
    
    def validate(self, value: Any) -> bool:
        return value is not None and value != ""


class MinLengthRule(ValidationRule):
    """Rule for minimum length"""
    
    def __init__(self, min_length: int, error_message: Optional[str] = None):
        super().__init__(error_message or f"Must be at least {min_length} characters long")
        self.min_length = min_length
    
    def validate(self, value: Any) -> bool:
        if not isinstance(value, (str, list, dict)):
            return False
        return len(value) >= self.min_length


class MaxLengthRule(ValidationRule):
    """Rule for maximum length"""
    
    def __init__(self, max_length: int, error_message: Optional[str] = None):
        super().__init__(error_message or f"Must be no more than {max_length} characters long")
        self.max_length = max_length
    
    def validate(self, value: Any) -> bool:
        if not isinstance(value, (str, list, dict)):
            return False
        return len(value) <= self.max_length


class PatternRule(ValidationRule):
    """Rule for regex pattern matching"""
    
    def __init__(self, pattern: str, error_message: Optional[str] = None):
        super().__init__(error_message or f"Must match pattern: {pattern}")
        self.pattern = re.compile(pattern)
    
    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return bool(self.pattern.match(value))


class RangeRule(ValidationRule):
    """Rule for numeric range validation"""
    
    def __init__(self, min_value: float, max_value: float, error_message: Optional[str] = None):
        super().__init__(error_message or f"Must be between {min_value} and {max_value}")
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> bool:
        try:
            num_value = float(value)
            return self.min_value <= num_value <= self.max_value
        except (ValueError, TypeError):
            return False


class EnumRule(ValidationRule):
    """Rule for enum value validation"""
    
    def __init__(self, enum_class: Type[Enum], error_message: Optional[str] = None):
        super().__init__(error_message or f"Must be one of: {[e.value for e in enum_class]}")
        self.enum_class = enum_class
    
    def validate(self, value: Any) -> bool:
        try:
            if isinstance(value, self.enum_class):
                return True
            return value in [e.value for e in self.enum_class]
        except (ValueError, TypeError):
            return False


class JSONRule(ValidationRule):
    """Rule for JSON validation"""
    
    def __init__(self, schema: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None):
        super().__init__(error_message or "Must be valid JSON")
        self.schema = schema
    
    def validate(self, value: Any) -> bool:
        if isinstance(value, str):
            try:
                json.loads(value)
                return True
            except json.JSONDecodeError:
                return False
        return isinstance(value, (dict, list))


class Validator:
    """
    Comprehensive validator for various data types and formats.
    """
    
    @staticmethod
    def validate_string(
        value: Any,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        field_name: str = "field"
    ) -> str:
        """
        Validate string input.
        
        Args:
            value: Value to validate
            required: Whether field is required
            min_length: Minimum length
            max_length: Maximum length
            pattern: Regex pattern to match
            field_name: Name of the field for error messages
            
        Returns:
            Validated string value
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and (value is None or value == ""):
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and empty
        if not required and (value is None or value == ""):
            return ""
        
        # Ensure it's a string
        if not isinstance(value, str):
            raise ValidationError(
                message=f"{field_name} must be a string",
                error_code="INVALID_TYPE",
                context={"field": field_name, "value": value, "expected_type": "string"}
            )
        
        # Validate length
        if min_length is not None and len(value) < min_length:
            raise ValidationError(
                message=f"{field_name} must be at least {min_length} characters long",
                error_code="MIN_LENGTH_ERROR",
                context={"field": field_name, "value": value, "min_length": min_length}
            )
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                message=f"{field_name} must be no more than {max_length} characters long",
                error_code="MAX_LENGTH_ERROR",
                context={"field": field_name, "value": value, "max_length": max_length}
            )
        
        # Validate pattern
        if pattern is not None:
            if not re.match(pattern, value):
                raise ValidationError(
                    message=f"{field_name} format is invalid",
                    error_code="PATTERN_ERROR",
                    context={"field": field_name, "value": value, "pattern": pattern}
                )
        
        return value.strip()
    
    @staticmethod
    def validate_integer(
        value: Any,
        required: bool = True,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        field_name: str = "field"
    ) -> int:
        """
        Validate integer input.
        
        Args:
            value: Value to validate
            required: Whether field is required
            min_value: Minimum value
            max_value: Maximum value
            field_name: Name of the field for error messages
            
        Returns:
            Validated integer value
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and value is None:
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and None
        if not required and value is None:
            return 0
        
        # Convert to integer
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(
                message=f"{field_name} must be an integer",
                error_code="INVALID_TYPE",
                context={"field": field_name, "value": value, "expected_type": "integer"}
            )
        
        # Validate range
        if min_value is not None and int_value < min_value:
            raise ValidationError(
                message=f"{field_name} must be at least {min_value}",
                error_code="MIN_VALUE_ERROR",
                context={"field": field_name, "value": int_value, "min_value": min_value}
            )
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(
                message=f"{field_name} must be no more than {max_value}",
                error_code="MAX_VALUE_ERROR",
                context={"field": field_name, "value": int_value, "max_value": max_value}
            )
        
        return int_value
    
    @staticmethod
    def validate_float(
        value: Any,
        required: bool = True,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        field_name: str = "field"
    ) -> float:
        """
        Validate float input.
        
        Args:
            value: Value to validate
            required: Whether field is required
            min_value: Minimum value
            max_value: Maximum value
            field_name: Name of the field for error messages
            
        Returns:
            Validated float value
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and value is None:
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and None
        if not required and value is None:
            return 0.0
        
        # Convert to float
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                message=f"{field_name} must be a number",
                error_code="INVALID_TYPE",
                context={"field": field_name, "value": value, "expected_type": "number"}
            )
        
        # Validate range
        if min_value is not None and float_value < min_value:
            raise ValidationError(
                message=f"{field_name} must be at least {min_value}",
                error_code="MIN_VALUE_ERROR",
                context={"field": field_name, "value": float_value, "min_value": min_value}
            )
        
        if max_value is not None and float_value > max_value:
            raise ValidationError(
                message=f"{field_name} must be no more than {max_value}",
                error_code="MAX_VALUE_ERROR",
                context={"field": field_name, "value": float_value, "max_value": max_value}
            )
        
        return float_value
    
    @staticmethod
    def validate_enum(
        value: Any,
        enum_class: Type[Enum],
        required: bool = True,
        field_name: str = "field"
    ) -> Enum:
        """
        Validate enum input.
        
        Args:
            value: Value to validate
            enum_class: Enum class to validate against
            required: Whether field is required
            field_name: Name of the field for error messages
            
        Returns:
            Validated enum value
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and value is None:
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and None
        if not required and value is None:
            return None
        
        # Validate enum value
        try:
            if isinstance(value, enum_class):
                return value
            return enum_class(value)
        except ValueError:
            valid_values = [e.value for e in enum_class]
            raise ValidationError(
                message=f"{field_name} must be one of: {valid_values}",
                error_code="INVALID_ENUM_VALUE",
                context={"field": field_name, "value": value, "valid_values": valid_values}
            )
    
    @staticmethod
    def validate_json(
        value: Any,
        required: bool = True,
        schema: Optional[Dict[str, Any]] = None,
        field_name: str = "field"
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Validate JSON input.
        
        Args:
            value: Value to validate
            required: Whether field is required
            schema: Optional JSON schema for validation
            field_name: Name of the field for error messages
            
        Returns:
            Validated JSON data
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and value is None:
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and None
        if not required and value is None:
            return {}
        
        # Parse JSON if string
        if isinstance(value, str):
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError as e:
                raise ValidationError(
                    message=f"{field_name} must be valid JSON: {str(e)}",
                    error_code="INVALID_JSON",
                    context={"field": field_name, "value": value, "json_error": str(e)}
                )
        else:
            parsed_value = value
        
        # Validate schema if provided
        if schema is not None:
            # Basic schema validation (could be enhanced with jsonschema library)
            if not isinstance(parsed_value, dict):
                raise ValidationError(
                    message=f"{field_name} must be a JSON object",
                    error_code="INVALID_JSON_SCHEMA",
                    context={"field": field_name, "value": parsed_value}
                )
        
        return parsed_value
    
    @staticmethod
    def validate_list(
        value: Any,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        item_type: Optional[Type] = None,
        field_name: str = "field"
    ) -> List[Any]:
        """
        Validate list input.
        
        Args:
            value: Value to validate
            required: Whether field is required
            min_length: Minimum length
            max_length: Maximum length
            item_type: Expected type for list items
            field_name: Name of the field for error messages
            
        Returns:
            Validated list
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if required and value is None:
            raise ValidationError(
                message=f"{field_name} is required",
                error_code="REQUIRED_FIELD",
                context={"field": field_name, "value": value}
            )
        
        # Skip validation if not required and None
        if not required and value is None:
            return []
        
        # Ensure it's a list
        if not isinstance(value, list):
            raise ValidationError(
                message=f"{field_name} must be a list",
                error_code="INVALID_TYPE",
                context={"field": field_name, "value": value, "expected_type": "list"}
            )
        
        # Validate length
        if min_length is not None and len(value) < min_length:
            raise ValidationError(
                message=f"{field_name} must have at least {min_length} items",
                error_code="MIN_LENGTH_ERROR",
                context={"field": field_name, "value": value, "min_length": min_length}
            )
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                message=f"{field_name} must have no more than {max_length} items",
                error_code="MAX_LENGTH_ERROR",
                context={"field": field_name, "value": value, "max_length": max_length}
            )
        
        # Validate item types
        if item_type is not None:
            for i, item in enumerate(value):
                if not isinstance(item, item_type):
                    raise ValidationError(
                        message=f"{field_name}[{i}] must be of type {item_type.__name__}",
                        error_code="INVALID_ITEM_TYPE",
                        context={"field": field_name, "index": i, "value": item, "expected_type": item_type.__name__}
                    )
        
        return value


class ModelValidator:
    """
    Validator for Pydantic models with enhanced error handling.
    """
    
    @staticmethod
    def validate_model(
        model_class: Type[BaseModel],
        data: Dict[str, Any],
        strict: bool = True
    ) -> BaseModel:
        """
        Validate data against a Pydantic model.
        
        Args:
            model_class: Pydantic model class
            data: Data to validate
            strict: Whether to use strict validation
            
        Returns:
            Validated model instance
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            if strict:
                return model_class(**data)
            else:
                return model_class.parse_obj(data)
        except PydanticValidationError as e:
            errors = []
            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                message = error["msg"]
                errors.append(f"{field}: {message}")
            
            raise ValidationError(
                message=f"Validation failed: {'; '.join(errors)}",
                error_code="MODEL_VALIDATION_ERROR",
                context={"model": model_class.__name__, "errors": errors, "data": data}
            )


class Sanitizer:
    """
    Data sanitization utilities.
    """
    
    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input.
        
        Args:
            value: String to sanitize
            max_length: Maximum length to truncate to
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return ""
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        # Truncate if necessary
        if max_length is not None and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def sanitize_json(value: Any) -> Any:
        """
        Sanitize JSON data.
        
        Args:
            value: JSON data to sanitize
            
        Returns:
            Sanitized JSON data
        """
        if isinstance(value, str):
            return Sanitizer.sanitize_string(value)
        elif isinstance(value, dict):
            return {k: Sanitizer.sanitize_json(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [Sanitizer.sanitize_json(item) for item in value]
        else:
            return value
