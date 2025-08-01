"""Simple Python client for the ChatGPT UI API."""

from typing import List, Optional, Tuple
import json
import time
import urllib.request

from .settings import API_BASE_URL


def _post_json(endpoint: str, payload: dict) -> Tuple[dict, float]:
    """Send a POST request with JSON and measure the response time."""
    url = f"{API_BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    start = time.time()
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
    duration = time.time() - start
    return json.loads(content), duration


def chat_completions(prompts: List[str], chat_url: Optional[str] = None) -> Tuple[List, float]:
    """Call the `/uia/chat/completions` endpoint."""
    payload = {"prompts": prompts}
    if chat_url is not None:
        payload["chat_url"] = chat_url
    response, duration = _post_json("/uia/chat/completions", payload)
    return response.get("articles", []), duration


def image_generations(prompts: List[str], chat_url: Optional[str] = None) -> Tuple[List, float]:
    """Call the `/uia/images/generations` endpoint."""
    payload = {"prompts": prompts}
    if chat_url is not None:
        payload["chat_url"] = chat_url
    response, duration = _post_json("/uia/images/generations", payload)
    return response.get("images", []), duration

