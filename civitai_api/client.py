import requests
from typing import Optional, Dict, Any
from .exceptions import CivitaiAPIError, RateLimitError
import urllib.parse
class CivitaiAPIClient:
    BASE_URL = "https://civitai.com/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
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

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = self._url_encode_query(params)
        #print(endpoint, params)
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        return self._request("DELETE", endpoint)
    
    def _url_encode_query(self,params, doseq=True):
        return urllib.parse.urlencode(params, doseq=True)