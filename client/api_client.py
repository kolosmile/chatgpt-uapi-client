"""Python client for the ChatGPT UI API."""

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

