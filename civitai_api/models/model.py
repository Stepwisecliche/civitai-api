"""Data models and enums for representing Civitai API models and their metadata.

This module defines classes for model types, creators, statistics, versions, and related enums.
"""

from dataclasses import dataclass
from enum import Enum


class ModelType(Enum):
    """Enumeration of supported model types in the Civitai API.

    Each value represents a distinct type of model that can be managed or retrieved.

    """

    CHECKPOINT = "Checkpoint"
    TEXTUAL_INVERSION = "TextualInversion"
    HYPERNETWORK = "Hypernetwork"
    AESTHETIC_GRADIENT = "AestheticGradient"
    LORA = "LORA"
    CONTROLNET = "Controlnet"
    POSES = "Poses"
    LoCon = "LoCon"
    WILDCARDS = "Wildcards"
    WORKFLOWS = "Workflows"
    OTHER = "Other"
    VAE = "VAE"
    MOTIONMODULE = "MotionModule"
    DoRA = "DoRA"


@dataclass
class ModelCreator:
    """Represents the creator of a model, including username and optional image."""

    username: str
    image: str | None


@dataclass
class ModelStats:
    """Represents statistics for a model, including downloads, favorites, comments, and ratings.

    Attributes:
        downloadCount (int): Number of times the model has been downloaded.
        favoriteCount (int): Number of times the model has been favorited.
        commentCount (int): Number of comments on the model.
        ratingCount (int): Number of ratings received.
        rating (float): Average rating of the model.

    """

    downloadCount: int
    favoriteCount: int
    commentCount: int
    ratingCount: int
    rating: float


@dataclass
class ModelVersion:
    """Represents a specific version of a model, including its version identifier and download URL.

    Attributes:
        version (str): The version identifier of the model.
        downloadUrl (str): The URL to download this version of the model.

    """

    version: str
    downloadUrl: str


class ModelMode(Enum):
    """Enumeration for the mode of a model, such as archived or taken down."""

    ARCHIVED = "Archived"
    TAKEN_DOWN = "TakenDown"


@dataclass
class Model:
    """Represents a Civitai model with its metadata, creator, statistics, and versions.

    Attributes:
        id (int): Unique identifier for the model.
        name (str): Name of the model.
        description (str): Description of the model.
        type (ModelType): Type of the model.
        nsfw (bool): Indicates if the model is NSFW.
        tags (List[str]): List of tags associated with the model.
        creator (ModelCreator): Creator information.
        stats (ModelStats): Model statistics.
        modelVersions (List[ModelVersion]): Available versions of the model.
        mode (Optional[ModelMode]): Mode of the model (e.g., archived, taken down).

    """

    id: int
    name: str
    description: str
    type: ModelType
    nsfw: bool
    tags: list[str]
    creator: ModelCreator
    stats: ModelStats
    modelVersions: list[ModelVersion]
    mode: ModelMode | None = None


class BaseModel(Enum):
    """Enumeration of supported base models in the Civitai API.

    Each value represents a distinct base model that can be referenced or used.

    """

    SD_1_4 = "SD 1.4"
    SD_1_5 = "SD 1.5"
    SD_1_5_LCM = "SD 1.5 LCM"
    SD_1_5_HYPER = "SD 1.5 Hyper"
    SD_2_0 = "SD 2.0"
    SD_2_1 = "SD 2.1"
    SDXL_1_0 = "SDXL 1.0"
    SD_3 = "SD 3"
    SDXL_TURBO = "SDXL Turbo"
    STABLE_CASCADE = "Stable Cascade"
    SVD = "SVD"
    SVD_XT = "SVD XT"
    PLAYGROUND_V2 = "Playground V2"
    PIXART_A = "PixArt A"
    PIXART_Σ = "PixArt Σ"  # noqa: PLC2401
    HUNYUAN_1 = "Hunyuan 1"
    LUMINA = "Lumina"
    OTHER = "Other"
