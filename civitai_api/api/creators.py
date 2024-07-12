from typing import List, Optional
from ..client import CivitaiAPIClient
from ..models.creator import Creator
from ..utils import parse_response, safe_get

class CreatorsAPI(CivitaiAPIClient):
    def list_creators(self, limit: Optional[int] = None, page: Optional[int] = None, query: Optional[str] = None) -> List[Creator]:
        """
        Get a list of creators.

        :param limit: The number of results to be returned per page (1-200, default 20)
        :param page: The page from which to start fetching creators
        :param query: Search query to filter creators by username
        :return: A list of Creator objects
        """
        params = {
            'limit': limit,
            'page': page,
            'query': query
        }
        response = self.get('creators', params={k: v for k, v in params.items() if v is not None})
        parsed_response = parse_response(response)
        
        creators = []
        for item in parsed_response['items']:
            creators.append(Creator(
                username=safe_get(item, 'username'),
                modelCount=safe_get(item, 'modelCount'),
                link=safe_get(item, 'link')
            ))
        
        return creators