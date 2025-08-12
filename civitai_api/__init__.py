"""Civitai API Client."""

from .api.creators import CreatorsAPI
from .api.images import ImagesAPI
from .api.model_versions import ModelVersionsAPI
from .api.models import ModelsAPI
from .api.tags import TagsAPI
from .client import CivitaiAPIClient, CivitaiAPIError, RateLimitError


class Civitai:
    """Civitai API client providing access to creators, images, models, model versions, and tags."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the Civitai API client with optional API key.

        Args:
            api_key (str | None): Optional API key for authentication.

        """
        # TODO: Implement global session singleton
        # TODO: Modify the parent class (CivitAPIClient) to take the session object
        # TODO: Implement context managers to handle session lifecycle and close connections after use.
        # TODO: Clean up the use of abstract methods. I think this code may be have been generated a bit,
        #   it has no consistent style.
        self.creators = CreatorsAPI(api_key)
        self.images = ImagesAPI(api_key)
        self.models = ModelsAPI(api_key)
        self.model_versions = ModelVersionsAPI(api_key)
        self.tags = TagsAPI(api_key)


__all__ = ["Civitai", "CivitaiAPIClient", "CivitaiAPIError", "RateLimitError"]
