# chatgpt-uapi-client

Python client for the ChatGPT UI API with optional JSON validation.

## Installation

```bash
pip install chatgpt-uapi-client

# With JSON validation support
pip install chatgpt-uapi-client[validation]
```

## Quick Start

```python
from gptuapi import GptClient

client = GptClient("http://localhost:8000")

# Simple text completion
articles, duration = client.chat_completions(["Hello!"])
print(articles[0])  # Response text

# Image generation
images, duration = client.image_generations(["A sunset over mountains"])
```

## JSON Mode (Structured Output)

Get validated JSON responses with automatic retry:

```python
from gptuapi import GptClient, JsonValidationError

client = GptClient("http://localhost:8000")

# Define expected response schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

# Get structured response
result, duration = client.chat_completions(
    prompts=["Generate a random person"],
    response_schema=schema,
    max_retries=3,  # Retry if validation fails
    strict=True     # Raise exception on failure
)

print(result)  # {"name": "John", "age": 25}
```

## API Reference

### `GptClient(api_base_url: str)`

Initialize client with API server URL.

### `client.chat_completions(prompts, chat_url=None, response_schema=None, max_retries=3, strict=True)`

**Parameters:**
- `prompts: List[str]` - List of prompts to send
- `chat_url: str | None` - Continue existing conversation
- `response_schema: dict | None` - JSON schema for validation (enables JSON mode)
- `max_retries: int` - Retry count on validation failure (default: 3)
- `strict: bool` - Raise `JsonValidationError` if True, return None if False

**Returns:** `Tuple[List | dict | None, float]` - (result, duration_seconds)

### `client.image_generations(prompts, chat_url=None)`

**Parameters:**
- `prompts: List[str]` - Image generation prompts
- `chat_url: str | None` - Continue existing conversation

**Returns:** `Tuple[List, float]` - (images list, duration_seconds)

## Exceptions

- `JsonValidationError` - Raised when JSON validation fails after all retries
  - `.errors: List[str]` - Validation error messages
  - `.attempts: int` - Number of attempts made
