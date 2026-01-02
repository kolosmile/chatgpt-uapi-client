"""JSON extraction and validation utilities for structured API responses.

This module provides functions for extracting JSON from text responses
and validating them against JSON schemas. It supports extracting JSON
from various formats including:
- Pure JSON strings
- Markdown code blocks (```json ... ```)
- JSON embedded within surrounding text

The validation functionality is optional and requires the `jsonschema`
package to be installed.

Example
-------
```python
from gptuapi.validator import extract_json, validate_json

text = 'Here is your data: {"name": "John", "age": 25} Hope this helps!'
data = extract_json(text)
# data = {"name": "John", "age": 25}

schema = {"type": "object", "required": ["name", "age"]}
is_valid, errors = validate_json(data, schema)
```
"""

import json
import re
from typing import Any, Optional, Tuple, List


def extract_json(text: str) -> Optional[dict]:
    """Extract JSON object from text, supporting various formats.
    
    Attempts to parse JSON from:
    1. Pure JSON string
    2. Markdown code block (```json ... ``` or ``` ... ```)
    3. JSON embedded in surrounding text
    
    Args:
        text: The text potentially containing JSON.
        
    Returns:
        Parsed JSON as a dict, or None if no valid JSON found.
    """
    if not text or not isinstance(text, str):
        return None
    
    text = text.strip()
    
    # Try 1: Pure JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try 2: Markdown code block
    # Match ```json ... ``` or ``` ... ```
    code_block_pattern = r'```(?:json)?\s*\n?([\s\S]*?)\n?```'
    matches = re.findall(code_block_pattern, text)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # Try 3: Find JSON object in text using balanced brace matching
    result = _find_json_object(text)
    if result is not None:
        return result
    
    return None


def _find_json_object(text: str) -> Optional[dict]:
    """Find and parse a JSON object within text using balanced brace matching.
    
    Args:
        text: Text that may contain a JSON object.
        
    Returns:
        Parsed JSON dict or None if not found.
    """
    start_idx = text.find('{')
    if start_idx == -1:
        return None
    
    # Find all potential JSON objects by tracking brace depth
    depth = 0
    json_start = None
    
    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                json_start = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and json_start is not None:
                candidate = text[json_start:i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    # This wasn't valid JSON, continue searching
                    json_start = None
                    continue
    
    return None


def validate_json(
    data: Any, 
    schema: dict
) -> Tuple[bool, List[str]]:
    """Validate data against a JSON schema.
    
    Args:
        data: The data to validate.
        schema: JSON Schema to validate against.
        
    Returns:
        Tuple of (is_valid, list of error messages).
        If jsonschema is not installed, returns (True, []) with a warning.
    """
    try:
        import jsonschema
    except ImportError:
        # jsonschema not installed - skip validation with warning
        return True, ["Warning: jsonschema not installed, validation skipped"]
    
    errors: List[str] = []
    
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, []
    except jsonschema.ValidationError as e:
        # Collect all errors using a validator
        validator = jsonschema.Draft7Validator(schema)
        for error in validator.iter_errors(data):
            path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
            errors.append(f"{path}: {error.message}")
        return False, errors
    except jsonschema.SchemaError as e:
        return False, [f"Invalid schema: {e.message}"]


class JsonValidationError(Exception):
    """Raised when JSON validation fails after all retries."""
    
    def __init__(self, message: str, errors: List[str], attempts: int):
        super().__init__(message)
        self.errors = errors
        self.attempts = attempts
