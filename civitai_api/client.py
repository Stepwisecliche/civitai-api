from abc import abstractmethod
import requests
from typing import Optional, Dict, Any, List, Union, TYPE_CHECKING
from .exceptions import CivitaiAPIError, RateLimitError
import urllib.parse
if TYPE_CHECKING:
    from civitai_api import Model, ModelType, ModelSort, ModelPeriod, BaseModel, ModelCategory, CommercialUse

class CivitaiAPIClient:
    BASE_URL = "https://civitai.com/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(self, endpoint_or_url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if endpoint_or_url.startswith('http'):
            url = endpoint_or_url
        else:
            url = f"{self.BASE_URL}/{endpoint_or_url.lstrip('/')}"
        
        params = self._url_encode_query(params) if params else None
        return self._request("GET", url, params=params)

    def _request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = self.session.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            raise CivitaiAPIError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise CivitaiAPIError(f"An error occurred: {e}")

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        return self._request("DELETE", endpoint)
    
    def _url_encode_query(self,params, doseq=True):
        return urllib.parse.urlencode(params, doseq=True)
    
    @abstractmethod
    def list_models(self, 
                    limit: Optional[int] = None, 
                    page: Optional[int] = None,
                    query: Optional[str] = None, 
                    tag: Optional[str] = None,
                    username: Optional[str] = None, 
                    types: Optional[List['ModelType']] = None,
                    sort: Optional['ModelSort'] = None, 
                    period: Optional['ModelPeriod'] = None,
                    rating: Optional[int] = None, 
                    favorites: Optional[bool] = None,
                    hidden: Optional[bool] = None, 
                    primary_file_only: Optional[bool] = None,
                    allow_no_credit: Optional[bool] = None, 
                    allow_derivatives: Optional[bool] = None,
                    allow_different_licenses: Optional[bool] = None,
                    base_models: Optional[List['BaseModel']] = None,
                    categories: Optional[List['ModelCategory']] = None,
                    allow_commercial_use: Optional[List['CommercialUse']] = None) -> List['Model']:
        """
        List models based on various filter criteria.
        This signature matches the CivitAI API for maximum compatibility.
        Firebase implementation may not use all parameters but should handle them gracefully.
        """
        pass

    @abstractmethod
    def get_model(self, model_id: Union[int, str]) -> Optional['Model']:
        """
        Retrieve a specific model by its ID.
        Uses Union[int, str] to accommodate both CivitAI (int) and Firebase (str) implementations.
        Returns Optional[Model] to handle cases where the model might not be found.
        """
        pass