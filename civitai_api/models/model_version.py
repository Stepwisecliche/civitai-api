from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class ModelVersionFile:
    name: str
    id: int
    sizeKb: float
    type: str
    format: str
    pickleScanResult: str
    pickleScanMessage: str
    virusScanResult: str
    scannedAt: Optional[datetime]
    hashes: Dict[str, str]
    downloadUrl: str

@dataclass
class ModelVersionImage:
    url: str
    nsfw: bool
    width: int
    height: int
    hash: str
    meta: Dict[str, Any]

@dataclass
class ModelVersionStats:
    downloadCount: int
    ratingCount: int
    rating: float

@dataclass
class ModelVersion:
    id: int
    modelId: int
    name: str
    createdAt: datetime
    downloadUrl: str
    trainedWords: List[str]
    baseModel: str
    files: List[ModelVersionFile]
    images: List[ModelVersionImage]
    stats: ModelVersionStats