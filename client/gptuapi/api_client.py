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

Example
-------

```python
from gptuapi import GptClient, API_BASE_URL

client = GptClient(API_BASE_URL)
messages, duration = client.chat_completions(["Hello!"])
```
"""

from typing import List, Optional, Tuple
import json
import time
import urllib.request


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

    def chat_completions(
        self, prompts: List[str], chat_url: Optional[str] = None
    ) -> Tuple[List, float]:
        """Call the `/uia/chat/completions` endpoint."""
        payload = {"prompts": prompts}
        if chat_url is not None:
            payload["chat_url"] = chat_url
        response, duration = self._post_json("/uia/chat/completions", payload)
        return response.get("articles", []), duration

    def image_generations(
        self, prompts: List[str], chat_url: Optional[str] = None
    ) -> Tuple[List, float]:
        """Call the `/uia/images/generations` endpoint."""
        payload = {"prompts": prompts}
        if chat_url is not None:
            payload["chat_url"] = chat_url
        response, duration = self._post_json("/uia/images/generations", payload)
        return response.get("images", []), duration

