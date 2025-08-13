"""Provides the TagsAPI class for interacting with tag-related endpoints.

Listing tags and parsing tag responses.
"""

from typing import Optional

from ..client import CivitaiAPIClient
from ..models.tag import Tag
from ..utils import parse_response, safe_get


class TagsAPI(CivitaiAPIClient):
    """API client for interacting with tags in the Civitai platform."""

    def list_tags(
        self,
        limit: int | None = None,
        page: int | None = None,
        query: str | None = None,
    ) -> list[Tag]:
        """Get a list of tags.

        :param limit: The number of results to be returned per page (1-200, default 20)
        :param page: The page from which to start fetching tags
        :param query: Search query to filter tags by name
        :return: A list of Tag objects
        """
        params = {"limit": limit, "page": page, "query": query}
        response = self.get(
            "tags", params={k: v for k, v in params.items() if v is not None}
        )
        parsed_response = parse_response(response)

        return [
            Tag(
                name=safe_get(item, "name"),
                modelCount=safe_get(item, "modelCount"),
                link=safe_get(item, "link"),
            )
            for item in parsed_response["items"]
        ]
