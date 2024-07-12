from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ModelType(Enum):
    CHECKPOINT = "Checkpoint"
    TEXTUAL_INVERSION = "TextualInversion"
    HYPERNETWORK = "Hypernetwork"
    AESTHETIC_GRADIENT = "AestheticGradient"
    LORA = "LORA"
    CONTROLNET = "Controlnet"
    POSES = "Poses"
    LYCORIS = "Lycoris"

class ModelMode(Enum):
    ARCHIVED = "Archived"
    TAKEN_DOWN = "TakenDown"

@dataclass
class ModelCreator:
    username: str
    image: Optional[str]

@dataclass
class ModelStats:
    downloadCount: int
    favoriteCount: int
    commentCount: int
    ratingCount: int
    rating: float

@dataclass
class ModelVersion:
    version: str
    downloadUrl: str

    def get_authenticated_download_url(self, token: str) -> str:
        """
        Returns an authenticated download URL by appending the provided token as a query parameter.

        :param token: The authentication token to be appended to the download URL
        :return: The authenticated download URL
        """
        return f"{self.downloadUrl}?token={token}"

@dataclass
class Model:
    id: int
    name: str
    description: str
    type: ModelType
    nsfw: bool
    tags: List[str]
    mode: Optional[ModelMode]
    creator: ModelCreator
    stats: ModelStats
    modelVersions: List[ModelVersion]  # Forward reference resolved

@dataclass
class BaseModel(Enum):
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
    PIXART_Σ = "PixArt Σ"
    HUNYUAN_1 = "Hunyuan 1"
    LUMINA = "Lumina"
    OTHER = "Other"