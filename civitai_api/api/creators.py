"""API module for interacting with Civitai creators.

Provides the CreatorsAPI class for listing and searching creators.
"""

from typing import Optional

from ..client import CivitaiAPIClient
from ..models.creator import Creator
from ..utils import parse_response, safe_get


class CreatorsAPI(CivitaiAPIClient):
    """API class for interacting with Civitai creators.

    Provides methods to list and search creators.

    """

    def list_creators(
        self,
        limit: int | None = None,
        page: int | None = None,
        query: str | None = None,
    ) -> list[Creator]:
        """Get a list of creators.

        :param limit: The number of results to be returned per page (1-200, default 20)
        :param page: The page from which to start fetching creators
        :param query: Search query to filter creators by username
        :return: A list of Creator objects
        """
        params = {
            "limit": limit,
            "page": page,
            "query": query,
        }
        response = self.get(
            "creators", params={k: v for k, v in params.items() if v is not None}
        )
        parsed_response = parse_response(response)

        return [
            Creator(
                username=safe_get(item, "username") or "",
                modelCount=int(safe_get(item, "modelCount") or 0),
                link=safe_get(item, "link") or "",
            )
            for item in parsed_response["items"]
        ]
