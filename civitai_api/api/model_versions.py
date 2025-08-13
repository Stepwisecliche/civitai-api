"""Provides the ModelVersionsAPI class for interacting with model version endpoints of the Civitai API.

It includes methods to retrieve model versions by ID or hash.
"""

from ..client import CivitaiAPIClient
from ..models.model_version import ModelVersion
from .models import ModelsAPI


class ModelVersionsAPI(CivitaiAPIClient):
    """Provides methods for interacting with model version endpoints of the Civitai API.

    This class allows retrieval of model versions by ID or hash.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize ModelVersions endpoint API.

        The class takes args and kwargs for initialization as a result of the parent.
        In our refactor pass, we will be modifying this and the other api classes to take the session object.
        Our init below is initializing the parent's __init__ method, which creates a session object.
        It is then creating a ModelsAPI class, which is doing the same thing. So contained in the
        parameters below, we have two unique session objects.

        The only actual argument being passed to these classes is the api_key to create the session.

        Our refactor will make this more inefficient.
        """
        super().__init__(*args, **kwargs)
        self._models_api = ModelsAPI(*args, **kwargs)

    def get_model_version(self, version_id: int) -> ModelVersion:
        """Get a specific model version by ID.

        :param version_id: The ID of the model version to retrieve
        :return: A ModelVersion object
        """
        response = self.get(f"model-versions/{version_id}")
        return self._models_api._parse_model_version(
            response
        )  # TODO: Fix accessing a private method of a private attribute.

    def get_model_version_by_hash(self, hash: str) -> ModelVersion:
        """Get a specific model version by hash.

        :param hash: The hash of the model version to retrieve (AutoV1, AutoV2, SHA256, CRC32, or Blake3)
        :return: A ModelVersion object
        """
        response = self.get(f"model-versions/by-hash/{hash}")
        return self._models_api._parse_model_version(
            response
        )  # TODO: Fix accessing a private method of a private attribute.
