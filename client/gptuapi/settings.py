"""Configuration settings for the API client."""


# Default API domain
API_BASE_URL = "http://localhost:8000"


def set_api_base_url(url: str) -> None:
    """Set the base URL for API requests."""
    global API_BASE_URL
    API_BASE_URL = url.rstrip("/")

