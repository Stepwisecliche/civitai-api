import urllib.parse
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Union

import requests

from .exceptions import CivitaiAPIError, RateLimitError

if TYPE_CHECKING:
    from civitai_api.models import (
        BaseModel,
        CommercialUse,
        Model,
        ModelCategory,
        ModelPeriod,
        ModelSort,
        ModelType,
    )


class CivitaiAPIClient:
    """Client for interacting with the CivitAI API.

    Provides methods for sending HTTP requests, handling authentication,
    and abstract methods for listing and retrieving models.
    """

    BASE_URL = "https://civitai.com/api/v1"

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the CivitaiAPIClient with an optional API key.

        Args:
            api_key (str | None): The API key for authentication. If provided, requests will include the Authorization header.

        """
        self.api_key = api_key
        # TODO(Joe): Child models are running super(), so every child model is creating a new session. This may be what is causing
        # issues with too many connections in the pool.
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(
        self,
        endpoint_or_url: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a GET request to the specified endpoint or URL.

        Args:
            endpoint_or_url (str): The API endpoint or full URL to send the request to.
            params (Optional[dict[str, Any]]): Optional query parameters to include in the request.

        Returns:
            dict[str, Any]: The JSON response from the API.

        Raises:
            CivitaiAPIError: If an HTTP or request error occurs.
            RateLimitError: If the API rate limit is exceeded.

        """
        if endpoint_or_url.startswith("http"):
            url = endpoint_or_url
        else:
            url = f"{self.BASE_URL}/{endpoint_or_url.lstrip('/')}"

        params = self._url_encode_query(params) if params else None
        return self._request("GET", url, params=params)

    def _request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send specified HTTP request and return decoded JSON response."""
        try:
            response = self.session.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                msg = "Rate limit exceeded"
                raise RateLimitError(msg) from e
            msg = f"HTTP error occurred: {e}"
            raise CivitaiAPIError(msg) from e
        except requests.exceptions.RequestException as e:
            msg = f"An error occurred: {e}"
            raise CivitaiAPIError(msg) from e

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request to the specified endpoint with the provided data.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (dict[str, Any]): The data to include in the POST request.

        Returns:
            dict[str, Any]: The JSON response from the API.

        """
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Send a PUT request to the specified endpoint with the provided data.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (dict[str, Any]): The data to include in the PUT request.

        Returns:
            dict[str, Any]: The JSON response from the API.

        """
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Send a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.

        Returns:
            dict[str, Any]: The JSON response from the API.

        """
        return self._request("DELETE", endpoint)

    def _url_encode_query(
        self, params: dict[str, Any]
    ) -> str:  # removed doseq kwarg from function arguments.
        # TODO(Joe): Learn about doseq to know why we need it to be true.
        return urllib.parse.urlencode(params, doseq=True)

    # TODO(Joe): why do we need this? For reference?
    @abstractmethod
    def list_models(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        query: Optional[str] = None,
        tag: Optional[str] = None,
        username: Optional[str] = None,
        types: Optional[list["ModelType"]] = None,
        sort: Optional["ModelSort"] = None,
        period: Optional["ModelPeriod"] = None,
        rating: Optional[int] = None,
        favorites: Optional[bool] = None,
        hidden: Optional[bool] = None,
        primary_file_only: Optional[bool] = None,
        allow_no_credit: Optional[bool] = None,
        allow_derivatives: Optional[bool] = None,
        allow_different_licenses: Optional[bool] = None,
        base_models: Optional[list["BaseModel"]] = None,
        categories: Optional[list["ModelCategory"]] = None,
        allow_commercial_use: Optional[list["CommercialUse"]] = None,
    ) -> list["Model"]:
        """List models based on various filter criteria.

        This signature matches the CivitAI API for maximum compatibility.
        Firebase implementation may not use all parameters but should handle them gracefully.
        """

    @abstractmethod
    def get_model(self, model_id: int | str) -> Optional["Model"]:
        """Retrieve a specific model by its ID.

        Uses Union[int, str] to accommodate both CivitAI (int) and Firebase (str) implementations.
        Returns Optional[Model] to handle cases where the model might not be found.
        """
