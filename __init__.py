"""Civitai API package.

This package provides classes and functions for interacting with the Civitai API,
including models, images, creators, and error handling.
"""

from .civitai_api import Civitai, CivitaiAPIClient
from .civitai_api.api.images import ImagePeriod, ImageSort
from .civitai_api.api.models import (
    CommercialUse,
    ModelCategory,
    ModelCreator,
    ModelPeriod,
    ModelSort,
)
from .civitai_api.exceptions import CivitaiAPIError, RateLimitError
from .civitai_api.models import Creator, Image, Model, ModelVersion, Tag
from .civitai_api.models.model import BaseModel, ModelMode, ModelStats, ModelType

__version__ = "0.1.0"

__all__ = [
    "BaseModel",
    "Civitai",
    "CivitaiAPIClient",
    "CivitaiAPIError",
    "CommercialUse",
    "Creator",
    "Image",
    "ImagePeriod",
    "ImageSort",
    "Model",
    "ModelCategory",
    "ModelCreator",
    "ModelMode",
    "ModelPeriod",
    "ModelSort",
    "ModelStats",
    "ModelType",
    "ModelVersion",
    "RateLimitError",
    "Tag",
]
