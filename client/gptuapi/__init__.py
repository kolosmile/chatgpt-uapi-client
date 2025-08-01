"""High level package for interacting with the ChatGPT UI API.

This package exposes the :class:`.GptClient` class which provides a thin
wrapper around the small REST API implemented by the `chatgpt-uapi` project.
The API mimics the behaviour of the ChatGPT web interface and can be useful
whenever the official OpenAI API is unavailable or lacks certain features.

Typical usage involves configuring the base URL of a running API server and
then instantiating :class:`~gptuapi.api_client.GptClient`::

    from gptuapi import GptClient, set_api_base_url, API_BASE_URL

    set_api_base_url("http://localhost:8000")
    client = GptClient(API_BASE_URL)
    articles, duration = client.chat_completions(["Hello!"])

The submodules ``api_client`` and ``settings`` are re-exported here for
convenience, so all public objects can be imported directly from
``gptuapi``.
"""

from .api_client import GptClient
from .settings import set_api_base_url, API_BASE_URL

__all__ = [
    "GptClient",
    "set_api_base_url",
    "API_BASE_URL",
]

