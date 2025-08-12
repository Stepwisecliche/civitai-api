"""Provide the ImagesAPI class and related enums for interacting with image resources from the Civitai API.

Includes functionality for listing images and specifying sorting/filtering options.
"""

from enum import Enum
from typing import Optional

from ..client import CivitaiAPIClient
from ..models.image import Image, ImageStats
from ..utils import parse_datetime, parse_response, safe_get


class ImageSort(Enum):
    """Enumeration for sorting options when listing images from the Civitai API."""

    MOST_REACTIONS = "Most Reactions"
    MOST_COMMENTS = "Most Comments"
    NEWEST = "Newest"


class ImagePeriod(Enum):
    """Enumeration for time periods used to filter or sort images from the Civitai API."""

    ALL_TIME = "AllTime"
    YEAR = "Year"
    MONTH = "Month"
    WEEK = "Week"
    DAY = "Day"


class ImagesAPI(CivitaiAPIClient):
    """API client for interacting with image resources from the Civitai API.

    Provides methods to list images and apply various filters and sorting options.
    """

    def list_images(
        self,
        limit: int | None = None,
        post_id: int | None = None,
        model_id: int | None = None,
        model_version_id: int | None = None,
        username: str | None = None,
        nsfw: bool | None = None,
        sort: ImageSort | None = None,
        period: ImagePeriod | None = None,
        page: int | None = None,
    ) -> list[Image]:
        """Get a list of images.

        :param limit: The number of results to be returned per page (1-200, default 100)
        :param post_id: The ID of a post to get images from
        :param model_id: The ID of a model to get images from (model gallery)
        :param model_version_id: The ID of a model version to get images from
        :param username: Filter to images from a specific user
        :param nsfw: Filter to images that contain mature content flags or not
        :param sort: The order in which to sort the results
        :param period: The time frame in which the images will be sorted
        :param page: The page from which to start fetching images
        :return: A list of Image objects
        """
        params = {
            "limit": limit,
            "postId": post_id,
            "modelId": model_id,
            "modelVersionId": model_version_id,
            "username": username,
            "nsfw": nsfw,
            "sort": sort.value if sort else None,
            "period": period.value if period else None,
            "page": page,
        }
        response = self.get(
            "images", params={k: v for k, v in params.items() if v is not None}
        )
        parsed_response = parse_response(response)

        images = [
            Image(
                id=safe_get(item, "id"),
                url=safe_get(item, "url"),
                hash=safe_get(item, "hash"),
                width=safe_get(item, "width"),
                height=safe_get(item, "height"),
                nsfw=safe_get(item, "nsfw"),
                createdAt=parse_datetime(safe_get(item, "createdAt")),
                postId=safe_get(item, "postId"),
                stats=ImageStats(
                    cryCount=safe_get(item["stats"], "cryCount"),
                    laughCount=safe_get(item["stats"], "laughCount"),
                    likeCount=safe_get(item["stats"], "likeCount"),
                    heartCount=safe_get(item["stats"], "heartCount"),
                    commentCount=safe_get(item["stats"], "commentCount"),
                ),
                meta=safe_get(item, "meta"),
                username=safe_get(item, "username"),
            )
            for item in parsed_response["items"]
        ]

        return images
