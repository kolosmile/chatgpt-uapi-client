"""Configuration helpers for the ChatGPT UI API client.

The module exposes a single setting, :data:`API_BASE_URL`, which defines the
HTTP address of the running API server. Clients may update this value at
runtime using :func:`set_api_base_url` before creating a
:class:`~gptuapi.api_client.GptClient` instance.

Example
-------

```python
from gptuapi import GptClient
from gptuapi.settings import set_api_base_url, API_BASE_URL

set_api_base_url("http://localhost:8000")
client = GptClient(API_BASE_URL)
```
"""


# Default API domain
API_BASE_URL = "http://localhost:8000"


def set_api_base_url(url: str) -> None:
    """Set the base URL for API requests."""
    global API_BASE_URL
    API_BASE_URL = url.rstrip("/")

