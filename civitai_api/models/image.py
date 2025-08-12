"""Data models for representing images and their statistics in the Civitai API."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ImageStats:
    """Statistics for an image, including reaction and comment counts."""

    cryCount: int
    laughCount: int
    likeCount: int
    heartCount: int
    commentCount: int


@dataclass
class Image:
    """Represents an image in the Civitai API.

    Attributes:
        id (int): Unique identifier for the image.
        url (str): URL of the image.
        hash (str): Hash of the image.
        width (int): Width of the image in pixels.
        height (int): Height of the image in pixels.
        nsfw (bool): Whether the image is not safe for work.
        createdAt (datetime): Timestamp when the image was created.
        postId (int): Identifier of the associated post.
        stats (ImageStats): Statistics related to the image.
        meta (dict[str, Any]): Additional metadata for the image.
        username (str): Username of the uploader.

    """

    id: int
    url: str
    hash: str
    width: int
    height: int
    nsfw: bool
    createdAt: datetime
    postId: int
    stats: ImageStats
    meta: dict[str, Any]
    username: str
