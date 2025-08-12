"""Data models for Civitai API model versions.

This module defines dataclasses for model version files, images, stats,
and the main ModelVersion entity.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ModelVersionFile:
    """Represents a file associated with a model version.

    Attributes:
        name (str): The name of the file.
        id (int): The unique identifier for the file.
        sizeKb (float): The size of the file in kilobytes.
        type (str): The type of the file.
        format (str): The format of the file.
        pickleScanResult (str): The result of the pickle scan.
        pickleScanMessage (str): The message from the pickle scan.
        virusScanResult (str): The result of the virus scan.
        scannedAt (Optional[datetime]): The datetime when the file was scanned.
        hashes (dict[str, str]): The hashes of the file.
        downloadUrl (str): The download URL for the file.
        primary (Optional[bool]): Whether this file is the primary file.

    """

    name: str
    id: int
    sizeKb: float
    type: str
    format: str
    pickleScanResult: str
    pickleScanMessage: str
    virusScanResult: str
    scannedAt: datetime | None
    hashes: dict[str, str]
    downloadUrl: str
    primary: bool | None


@dataclass
class ModelVersionImage:
    """Represents an image associated with a model version.

    Attributes:
        url (str): The URL of the image.
        nsfw (bool): Whether the image is not safe for work.
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        hash (str): The hash of the image.
        meta (dict[str, Any]): Additional metadata for the image.

    """

    url: str
    nsfw: bool
    width: int
    height: int
    hash: str
    meta: dict[str, Any]


@dataclass
class ModelVersionStats:
    """Represents statistics for a model version.

    Attributes:
        downloadCount (int): The number of times the model version has been downloaded.
        ratingCount (int): The number of ratings received.
        rating (float): The average rating.

    """

    downloadCount: int
    ratingCount: int
    rating: float


@dataclass
class ModelVersion:
    """Represents a version of a model in the Civitai API.

    Attributes:
        id (int): The unique identifier for the model version.
        modelId (int): The identifier of the parent model.
        name (str): The name of the model version.
        createdAt (datetime): The creation date and time of the model version.
        downloadUrl (str): The download URL for the model version.
        trainedWords (list[str]): Words the model was trained on.
        baseModel (str): The base model used.
        files (list[ModelVersionFile]): Files associated with the model version.
        images (list[ModelVersionImage]): Images associated with the model version.
        stats (ModelVersionStats): Statistics for the model version.

    """

    id: int
    modelId: int
    name: str
    createdAt: datetime
    downloadUrl: str
    trainedWords: list[str]
    baseModel: str
    files: list[ModelVersionFile]
    images: list[ModelVersionImage]
    stats: ModelVersionStats
