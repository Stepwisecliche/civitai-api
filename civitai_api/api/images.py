from typing import List, Optional
from ..client import CivitaiAPIClient
from ..models.image import Image, ImageStats
from ..utils import parse_response, parse_datetime, safe_get
from enum import Enum

class ImageSort(Enum):
    MOST_REACTIONS = "Most Reactions"
    MOST_COMMENTS = "Most Comments"
    NEWEST = "Newest"

class ImagePeriod(Enum):
    ALL_TIME = "AllTime"
    YEAR = "Year"
    MONTH = "Month"
    WEEK = "Week"
    DAY = "Day"

class ImagesAPI(CivitaiAPIClient):
    def list_images(self, limit: Optional[int] = None, post_id: Optional[int] = None,
                    model_id: Optional[int] = None, model_version_id: Optional[int] = None,
                    username: Optional[str] = None, nsfw: Optional[bool] = None,
                    sort: Optional[ImageSort] = None, period: Optional[ImagePeriod] = None,
                    page: Optional[int] = None) -> List[Image]:
        """
        Get a list of images.

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
            'limit': limit,
            'postId': post_id,
            'modelId': model_id,
            'modelVersionId': model_version_id,
            'username': username,
            'nsfw': nsfw,
            'sort': sort.value if sort else None,
            'period': period.value if period else None,
            'page': page
        }
        response = self.get('images', params={k: v for k, v in params.items() if v is not None})
        parsed_response = parse_response(response)
        
        images = []
        for item in parsed_response['items']:
            images.append(Image(
                id=safe_get(item, 'id'),
                url=safe_get(item, 'url'),
                hash=safe_get(item, 'hash'),
                width=safe_get(item, 'width'),
                height=safe_get(item, 'height'),
                nsfw=safe_get(item, 'nsfw'),
                createdAt=parse_datetime(safe_get(item, 'createdAt')),
                postId=safe_get(item, 'postId'),
                stats=ImageStats(
                    cryCount=safe_get(item['stats'], 'cryCount'),
                    laughCount=safe_get(item['stats'], 'laughCount'),
                    likeCount=safe_get(item['stats'], 'likeCount'),
                    heartCount=safe_get(item['stats'], 'heartCount'),
                    commentCount=safe_get(item['stats'], 'commentCount')
                ),
                meta=safe_get(item, 'meta'),
                username=safe_get(item, 'username')
            ))
        
        return images