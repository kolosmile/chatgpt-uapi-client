"""Python client for the ChatGPT UI API.

The module defines :class:`GptClient`, a lightweight wrapper around the REST
endpoints exposed by the ChatGPT UI automation server. Each method makes an
HTTP request to the configured server and returns both the parsed JSON payload
and the time taken for the request.

Supported endpoints
-------------------

- ``/uia/chat/completions`` – send one or more prompts and receive the
  corresponding text responses.
- ``/uia/images/generations`` – generate images via the ChatGPT UI.

Both endpoints accept a list of prompt strings. A ``chat_url`` parameter may be
supplied to continue an existing conversation. Methods return a tuple of the
resulting list (``articles`` or ``images``) and the elapsed time in seconds.

JSON Mode
---------

The ``chat_completions`` method supports optional JSON response validation:

```python
from gptuapi import GptClient

client = GptClient("http://localhost:8000")
result, duration = client.chat_completions(
    prompts=["Give me a person with name and age"],
    response_schema={"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name", "age"]},
    max_retries=3,
    strict=True
)
# result = {"name": "John", "age": 25}
```
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import json
import time
import urllib.request

from .validator import extract_json, validate_json, JsonValidationError


class GptClient:
    """Client for calling the ChatGPT UI API."""

    def __init__(self, api_base_url: str) -> None:
        self.api_base_url = api_base_url.rstrip("/")

    def _post_json(self, endpoint: str, payload: dict) -> Tuple[dict, float]:
        """Send a POST request with JSON and measure the response time."""
        url = f"{self.api_base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        start = time.time()
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
        duration = time.time() - start
        return json.loads(content), duration

    def _build_json_prompt(
        self, 
        prompt: str, 
        schema: dict, 
        errors: Optional[List[str]] = None
    ) -> str:
        """Build prompt with JSON schema instructions and optional error feedback."""
        parts = []
        
        if errors:
            parts.append("Your previous response had validation errors:")
            for error in errors:
                parts.append(f"- {error}")
            parts.append("")
            parts.append("Please fix and respond again.")
            parts.append("")
        
        parts.append(prompt)
        parts.append("")
        parts.append("Respond ONLY with valid JSON matching this schema:")
        parts.append(json.dumps(schema, indent=2))
        
        return "\n".join(parts)

    def chat_completions(
        self,
        prompts: List[str],
        chat_url: Optional[str] = None,
        response_schema: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        strict: bool = True,
    ) -> Tuple[Union[List, Dict, None], float]:
        """Call the `/uia/chat/completions` endpoint.
        
        Args:
            prompts: List of prompt strings to send.
            chat_url: Optional URL to continue an existing conversation.
            response_schema: Optional JSON schema to validate the response against.
                If provided, enables JSON mode with automatic retry on validation failure.
            max_retries: Maximum number of retry attempts if validation fails (default: 3).
            strict: If True, raise JsonValidationError on validation failure.
                If False, return None instead.
        
        Returns:
            Tuple of (result, duration).
            - Without response_schema: result is List of articles
            - With response_schema: result is the validated dict, or None if strict=False and validation failed
        """
        total_start = time.time()
        
        # Standard mode (no JSON validation)
        if response_schema is None:
            payload = {"prompts": prompts}
            if chat_url is not None:
                payload["chat_url"] = chat_url
            response, duration = self._post_json("/uia/chat/completions", payload)
            return response.get("articles", []), duration
        
        # JSON mode with validation
        original_prompt = prompts[0] if prompts else ""
        current_chat_url = chat_url
        last_errors: List[str] = []
        
        for attempt in range(max_retries):
            # Build prompt with schema (and errors if retry)
            augmented_prompt = self._build_json_prompt(
                original_prompt, 
                response_schema, 
                last_errors if attempt > 0 else None
            )
            
            payload = {"prompts": [augmented_prompt]}
            if current_chat_url is not None:
                payload["chat_url"] = current_chat_url
            
            response, _ = self._post_json("/uia/chat/completions", payload)
            articles = response.get("articles", [])
            
            # Update chat_url for subsequent retries (continue conversation)
            if "chat_url" in response:
                current_chat_url = response["chat_url"]
            
            # Extract and validate JSON from response
            if articles:
                # Get the text content from the first article
                article = articles[0]
                # Article can be a list of strings (line-by-line) or a single string
                if isinstance(article, list):
                    # Join all string elements, skipping metadata like "ChatGPT said:" and "Copy code"
                    text = "\n".join(str(item) for item in article)
                else:
                    text = str(article)
                
                extracted = extract_json(text)
                if extracted is not None:
                    is_valid, errors = validate_json(extracted, response_schema)
                    if is_valid:
                        total_duration = time.time() - total_start
                        return extracted, total_duration
                    else:
                        last_errors = errors
                else:
                    last_errors = ["Could not extract valid JSON from response"]
            else:
                last_errors = ["No response received"]
        
        # All retries exhausted
        total_duration = time.time() - total_start
        if strict:
            raise JsonValidationError(
                f"Failed to get valid JSON response after {max_retries} attempts",
                last_errors,
                max_retries
            )
        return None, total_duration

    def image_generations(
        self, prompts: List[str], chat_url: Optional[str] = None
    ) -> Tuple[List, float]:
        """Call the `/uia/images/generations` endpoint."""
        payload = {"prompts": prompts}
        if chat_url is not None:
            payload["chat_url"] = chat_url
        response, duration = self._post_json("/uia/images/generations", payload)
        return response.get("images", []), duration
