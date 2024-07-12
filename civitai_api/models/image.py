from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass
class ImageStats:
    cryCount: int
    laughCount: int
    likeCount: int
    heartCount: int
    commentCount: int

@dataclass
class Image:
    id: int
    url: str
    hash: str
    width: int
    height: int
    nsfw: bool
    createdAt: datetime
    postId: int
    stats: ImageStats
    meta: Dict[str, Any]
    username: str