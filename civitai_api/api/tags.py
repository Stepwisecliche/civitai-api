from typing import List, Optional
from ..client import CivitaiAPIClient
from ..models.tag import Tag
from ..utils import parse_response, safe_get

class TagsAPI(CivitaiAPIClient):
    def list_tags(self, limit: Optional[int] = None, page: Optional[int] = None, query: Optional[str] = None) -> List[Tag]:
        """
        Get a list of tags.

        :param limit: The number of results to be returned per page (1-200, default 20)
        :param page: The page from which to start fetching tags
        :param query: Search query to filter tags by name
        :return: A list of Tag objects
        """
        params = {
            'limit': limit,
            'page': page,
            'query': query
        }
        response = self.get('tags', params={k: v for k, v in params.items() if v is not None})
        parsed_response = parse_response(response)
        
        tags = []
        for item in parsed_response['items']:
            tags.append(Tag(
                name=safe_get(item, 'name'),
                modelCount=safe_get(item, 'modelCount'),
                link=safe_get(item, 'link')
            ))
        
        return tags