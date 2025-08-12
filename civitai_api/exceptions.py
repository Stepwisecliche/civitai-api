"""Exceptions for Civitai API errors.

Custom exceptions for handling errors related to the Civitai API.
"""


class CivitaiAPIError(Exception):
    """Base exception for Civitai API errors."""


class RateLimitError(CivitaiAPIError):
    """Raised when rate limit is exceeded."""
