"""Provides the ModelsAPI class and related enums for interacting with the Civitai API.

It includes functionality for listing models, retrieving model details, and parsing model data.
"""

import logging
from collections.abc import Generator
from enum import Enum
from typing import Any, Optional, Union
from urllib.parse import parse_qsl, urlparse

from ..client import CivitaiAPIClient
from ..models.model import (
    BaseModel,
    Model,
    ModelCreator,
    ModelMode,
    ModelStats,
    ModelType,
)
from ..models.model_version import (
    ModelVersion,
    ModelVersionFile,
    ModelVersionImage,
    ModelVersionStats,
)
from ..utils import create_enum_list, parse_datetime, parse_response, safe_get


class ModelSort(Enum):
    """Enumeration for sorting models in the Civitai API.

    Options include highest rated, most downloaded, and newest models.
    """

    HIGHEST_RATED = "Highest Rated"
    MOST_DOWNLOADED = "Most Downloaded"
    NEWEST = "Newest"


class ModelPeriod(Enum):
    """Enumeration for time periods in the Civitai API.

    Options include all time, year, month, week, and day.
    """

    ALL_TIME = "AllTime"
    YEAR = "Year"
    MONTH = "Month"
    WEEK = "Week"
    DAY = "Day"


class ModelCategory(Enum):
    """Enumeration for model categories in the Civitai API.

    Options include various categories such as action, animal, assets, and more.
    """

    ACTION = "Action"
    ANIMAL = "Animal"
    ASSETS = "Assets"
    BACKGROUND = "Background"
    BASE_MODEL = "Base Model"
    BUILDINGS = "Buildings"
    CELEBRITY = "Celebrity"
    CHARACTER = "Character"
    CLOTHING = "Clothing"
    CONCEPT = "Concept"
    GUIDE = "Guide"
    OBJECTS = "Objects"
    POSES = "Poses"
    STYLE = "Style"
    TOOL = "Tool"
    VEHICLE = "Vehicle"


class CommercialUse(Enum):
    """Enumeration for commercial use options in the Civitai API.

    Options include none, image, rent, and sell.
    """

    NONE = "None"
    IMAGE = "Image"
    RENT = "Rent"
    SELL = "Sell"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelsAPI(CivitaiAPIClient):
    """API client for interacting with models in the Civitai platform."""

    def list_models(
        self,
        limit: int | None = 100,
        page: int | None = 1,
        query: str | None = None,
        tag: str | None = None,
        username: str | None = None,
        types: list[ModelType] | None = None,
        sort: ModelSort | None = None,
        period: ModelPeriod | None = None,
        rating: int | None = None,
        favorites: bool | None = None,
        hidden: bool | None = None,
        primary_file_only: bool | None = None,
        allow_no_credit: bool | None = None,
        allow_derivatives: bool | None = None,
        allow_different_licenses: bool | None = None,
        base_models: list[BaseModel] | None = None,
        categories: list[ModelCategory] | None = None,
        allow_commercial_use: list[CommercialUse] | None = None,
    ) -> Generator[list[Model], None, None]:

        print("DEBUG: Entering modified list_models method")

        url = f"{self.BASE_URL}/models"
        params = self._construct_params(locals())

        while True:
            print(f"DEBUG: Fetching URL: {url}")
            print(f"DEBUG: Params: {params}")

            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            models = self._parse_models(data.get("items", []))
            yield models

            metadata = data.get("metadata", {})
            print(f"DEBUG: Metadata: {metadata}")

            next_page_url = metadata.get("nextPage")
            print(f"DEBUG: Next page URL: {next_page_url}")

            if next_page_url:
                parsed_url = urlparse(next_page_url)
                url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                params = dict(parse_qsl(parsed_url.query))
            else:
                print("DEBUG: No more pages available")
                break

    def _construct_params(self, kwargs: dict) -> dict[str, Any]:
        params = {
            "limit": kwargs.get("limit"),
            "page": kwargs.get("page"),
            "query": kwargs.get("query"),
            "tag": kwargs.get("tag"),
            "username": kwargs.get("username"),
            "modelType": (
                [t.value for t in kwargs.get("types", [])]
                if kwargs.get("types")
                else None
            ),
            "sortBy": kwargs.get("sort").value if kwargs.get("sort") else None,
            "period": kwargs.get("period").value if kwargs.get("period") else None,
            "rating": kwargs.get("rating"),
            "favorites": kwargs.get("favorites"),
            "hidden": kwargs.get("hidden"),
            "primaryFileOnly": kwargs.get("primary_file_only"),
            "allowNoCredit": kwargs.get("allow_no_credit"),
            "allowDerivatives": kwargs.get("allow_derivatives"),
            "allowDifferentLicenses": kwargs.get("allow_different_licenses"),
            "baseModel": (
                [m.value for m in kwargs.get("base_models", [])]
                if kwargs.get("base_models")
                else None
            ),
            "category": (
                [c.value for c in kwargs.get("categories", [])]
                if kwargs.get("categories")
                else None
            ),
        }

        # Handle allowCommercialUse as a list of values
        if kwargs.get("allow_commercial_use"):
            for i, use in enumerate(kwargs["allow_commercial_use"]):
                params[f"allowCommercialUse[{i}]"] = use.value

        return {k: v for k, v in params.items() if v is not None}

    def get_model(self, model_id: int | str) -> Model:
        """Fetch a model by its ID."""
        response = self.get(f"/models/{model_id}")

        m = Model(
            id=safe_get(response, "id"),
            name=safe_get(response, "name"),
            description=safe_get(response, "description"),
            type=ModelType(safe_get(response, "type")),
            nsfw=safe_get(response, "nsfw"),
            tags=safe_get(response, "tags"),
            mode=(
                ModelMode(safe_get(response, "mode"))
                if safe_get(response, "mode")
                else None
            ),
            creator=ModelCreator(
                username=safe_get(response.get("creator", {}), "username"),
                image=safe_get(response.get("creator", {}), "image"),
            ),
            stats=ModelStats(
                downloadCount=safe_get(response.get("stats", {}), "downloadCount"),
                favoriteCount=safe_get(response.get("stats", {}), "favoriteCount"),
                commentCount=safe_get(response.get("stats", {}), "commentCount"),
                ratingCount=safe_get(response.get("stats", {}), "ratingCount"),
                rating=safe_get(response.get("stats", {}), "rating"),
            ),
            modelVersions=[
                self._parse_model_version(v)
                for v in safe_get(response, "modelVersions")
            ],
        )
        return m

    def _parse_models(self, items: list[dict]) -> list[Model]:
        models = []
        for item in items:
            models.append(
                Model(
                    id=safe_get(item, "id"),
                    name=safe_get(item, "name"),
                    description=safe_get(item, "description"),
                    type=ModelType(safe_get(item, "type")),
                    nsfw=safe_get(item, "nsfw"),
                    tags=safe_get(item, "tags"),
                    mode=(
                        ModelMode(safe_get(item, "mode"))
                        if safe_get(item, "mode")
                        else None
                    ),
                    creator=ModelCreator(
                        username=safe_get(item.get("creator", {}), "username"),
                        image=safe_get(item.get("creator", {}), "image"),
                    ),
                    stats=ModelStats(
                        downloadCount=safe_get(item.get("stats", {}), "downloadCount"),
                        favoriteCount=safe_get(item.get("stats", {}), "favoriteCount"),
                        commentCount=safe_get(item.get("stats", {}), "commentCount"),
                        ratingCount=safe_get(item.get("stats", {}), "ratingCount"),
                        rating=safe_get(item.get("stats", {}), "rating"),
                    ),
                    modelVersions=[
                        self._parse_model_version(v)
                        for v in safe_get(item, "modelVersions")
                    ],
                )
            )
        return models

    def _parse_model_version(self, version: dict) -> ModelVersion:
        created_at_str = safe_get(version, "createdAt")
        created_at = parse_datetime(created_at_str) if created_at_str else None
        if safe_get(version, "images"):
            images = [
                ModelVersionImage(
                    url=safe_get(i, "url"),
                    nsfw=safe_get(i, "nsfw"),
                    width=safe_get(i, "width"),
                    height=safe_get(i, "height"),
                    hash=safe_get(i, "hash"),
                    meta=safe_get(i, "meta"),
                )
                for i in safe_get(version, "images")
            ]
        else:
            images = None
        return ModelVersion(
            id=safe_get(version, "id"),
            modelId=safe_get(version, "modelId"),
            name=safe_get(version, "name"),
            createdAt=created_at,
            downloadUrl=safe_get(version, "downloadUrl"),
            trainedWords=safe_get(version, "trainedWords"),
            baseModel=safe_get(version, "baseModel"),
            files=[
                ModelVersionFile(
                    name=safe_get(f, "name"),
                    id=safe_get(f, "id"),
                    sizeKb=safe_get(f, "sizeKB"),
                    type=safe_get(f, "type"),
                    format=safe_get(f, "format"),
                    pickleScanResult=safe_get(f, "pickleScanResult"),
                    pickleScanMessage=safe_get(f, "pickleScanMessage"),
                    virusScanResult=safe_get(f, "virusScanResult"),
                    scannedAt=(
                        parse_datetime(safe_get(f, "scannedAt"))
                        if safe_get(f, "scannedAt")
                        else None
                    ),
                    hashes=safe_get(f, "hashes"),
                    downloadUrl=safe_get(f, "downloadUrl"),
                    primary=safe_get(f, "primary"),
                )
                for f in safe_get(version, "files")
            ],
            images=images,
            stats=ModelVersionStats(
                downloadCount=safe_get(version.get("stats", {}), "downloadCount"),
                ratingCount=safe_get(version.get("stats", {}), "ratingCount"),
                rating=safe_get(version.get("stats", {}), "rating"),
            ),
        )
