"""
This module provides the ModelVersionsAPI class for interacting with model version endpoints
of the Civitai API. It includes methods to retrieve model versions by ID or hash.
"""

from ..client import CivitaiAPIClient
from ..models.model_version import ModelVersion
from .models import ModelsAPI


class ModelVersionsAPI(CivitaiAPIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._models_api = ModelsAPI(*args, **kwargs)

    def get_model_version(self, version_id: int) -> ModelVersion:
        """
        Get a specific model version by ID.

        :param version_id: The ID of the model version to retrieve
        :return: A ModelVersion object
        """
        response = self.get(f'model-versions/{version_id}')
        return self._models_api._parse_model_version(response)

    def get_model_version_by_hash(self, hash: str) -> ModelVersion:
        """
        Get a specific model version by hash.

        :param hash: The hash of the model version to retrieve (AutoV1, AutoV2, SHA256, CRC32, or Blake3)
        :return: A ModelVersion object
        """
        response = self.get(f'model-versions/by-hash/{hash}')
        return self._models_api._parse_model_version(response)