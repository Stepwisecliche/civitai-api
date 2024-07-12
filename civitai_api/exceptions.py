class CivitaiAPIError(Exception):
    """Base exception for Civitai API errors"""
    pass

class RateLimitError(CivitaiAPIError):
    """Raised when rate limit is exceeded"""
    pass