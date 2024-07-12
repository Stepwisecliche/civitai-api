from .api.creators import CreatorsAPI
from .api.images import ImagesAPI
from .api.models import ModelsAPI
from .api.model_versions import ModelVersionsAPI
from .api.tags import TagsAPI
from typing import Optional

class Civitai:
    def __init__(self, api_key: Optional[str] = None):
        self.creators = CreatorsAPI(api_key)
        self.images = ImagesAPI(api_key)
        self.models = ModelsAPI(api_key)
        self.model_versions = ModelVersionsAPI(api_key)
        self.tags = TagsAPI(api_key)

__all__ = ['Civitai']