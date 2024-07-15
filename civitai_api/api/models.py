from typing import List, Optional
from ..client import CivitaiAPIClient
from ..models.model import Model, ModelType, ModelMode, ModelCreator, ModelStats, BaseModel
from ..models.model_version import ModelVersion, ModelVersionFile, ModelVersionImage, ModelVersionStats
from ..utils import parse_response, parse_datetime, create_enum_list, safe_get
from enum import Enum

class ModelSort(Enum):
    HIGHEST_RATED = "Highest Rated"
    MOST_DOWNLOADED = "Most Downloaded"
    NEWEST = "Newest"

class ModelPeriod(Enum):
    ALL_TIME = "AllTime"
    YEAR = "Year"
    MONTH = "Month"
    WEEK = "Week"
    DAY = "Day"

class ModelCategory(Enum):
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
    NONE = "None"
    IMAGE = "Image"
    RENT = "Rent"
    SELL = "Sell"

class ModelsAPI(CivitaiAPIClient):
    def list_models(self, limit: Optional[int] = None, page: Optional[int] = None,
                    query: Optional[str] = None, tag: Optional[str] = None,
                    username: Optional[str] = None, types: Optional[List[ModelType]] = None,
                    sort: Optional[ModelSort] = None, period: Optional[ModelPeriod] = None,
                    rating: Optional[int] = None, favorites: Optional[bool] = None,
                    hidden: Optional[bool] = None, primary_file_only: Optional[bool] = None,
                    allow_no_credit: Optional[bool] = None, allow_derivatives: Optional[bool] = None,
                    allow_different_licenses: Optional[bool] = None,
                    base_models: Optional[List[BaseModel]] = None,
                    categories: Optional[List[ModelCategory]] = None,
                    allow_commercial_use: Optional[List[CommercialUse]] = None) -> List[Model]:
        
        """
        Get a list of models.

        :param limit: The number of results to be returned per page (1-200, default 100)
        :param page: The page from which to start fetching models
        :param query: Search query to filter models by name
        :param tag: Search query to filter models by tag
        :param username: Search query to filter models by user
        :param types: The type of model to filter with
        :param sort: The order in which to sort the results
        :param period: The time frame in which the models will be sorted
        :param rating: The rating to filter the models with
        :param favorites: Filter to favorites of the authenticated user
        :param hidden: Filter to hidden models of the authenticated user
        :param primary_file_only: Only include the primary file for each model
        :param allow_no_credit: Filter to models that require or don't require crediting
        :param allow_derivatives: Filter to models that allow or don't allow creating derivatives
        :param allow_different_licenses: Filter to models that allow or don't allow derivatives to have a different license
        :param allow_commercial_use: Filter to models based on their commercial permissions
        :param categories: Filter to models based on their category
        :return: A list of Model objects
        """
        params = {
            'limit': limit,
            'page': page,
            'query': query,
            'tag': tag,
            'username': username,
            'modelType': [t.value for t in types] if types else None,
            'sortBy': sort.value if sort else None,
            'period': period.value if period else None,
            'rating': rating,
            'favorites': favorites,
            'hidden': hidden,
            'primaryFileOnly': primary_file_only,
            'allowNoCredit': allow_no_credit,
            'allowDerivatives': allow_derivatives,
            'allowDifferentLicenses': allow_different_licenses,
            'baseModel': [m.value for m in base_models] if base_models else None,
            'category': [c.value for c in categories] if categories else None
        }

        # Handle allowCommercialUse as a list of values
        if allow_commercial_use:
            for i, use in enumerate(allow_commercial_use):
                params[f'allowCommercialUse[{i}]'] = use.value

        response = self.get('models', params={k: v for k, v in params.items() if v is not None})

        parsed_response = parse_response(response)
        
        models = self._parse_models(parsed_response.get('items', []))

        # Filter models based on base_models parameter
        # if base_models:
        #     models = [model for model in models if any(version.baseModel in [bm.value for bm in base_models] for version in model.modelVersions)]

        return models


    def get_model(self, model_id: int) -> Model:
        """
        Get a specific model by ID.

        :param model_id: The ID of the model to retrieve
        :return: A Model object
        """
        response = self.get(f'models/{model_id}')
        return self._parse_models([response])[0]

    def _parse_models(self, items: List[dict]) -> List[Model]:
        models = []
        for item in items:
            models.append(Model(
                id=safe_get(item, 'id'),
                name=safe_get(item, 'name'),
                description=safe_get(item, 'description'),
                type=ModelType(safe_get(item, 'type')),
                nsfw=safe_get(item, 'nsfw'),
                tags=safe_get(item, 'tags'),
                mode=ModelMode(safe_get(item, 'mode')) if safe_get(item, 'mode') else None,
                creator=ModelCreator(
                    username=safe_get(item.get('creator', {}), 'username'),
                    image=safe_get(item.get('creator', {}), 'image')
                ),
                stats=ModelStats(
                    downloadCount=safe_get(item.get('stats', {}), 'downloadCount'),
                    favoriteCount=safe_get(item.get('stats', {}), 'favoriteCount'),
                    commentCount=safe_get(item.get('stats', {}), 'commentCount'),
                    ratingCount=safe_get(item.get('stats', {}), 'ratingCount'),
                    rating=safe_get(item.get('stats', {}), 'rating')
                ),
                modelVersions=[self._parse_model_version(v) for v in safe_get(item, 'modelVersions')]
            ))
        return models

    def _parse_model_version(self, version: dict) -> ModelVersion:
        created_at_str = safe_get(version, 'createdAt')
        created_at = parse_datetime(created_at_str) if created_at_str else None

        return ModelVersion(
            id=safe_get(version, 'id'),
            modelId=safe_get(version, 'modelId'),
            name=safe_get(version, 'name'),
            createdAt=created_at,
            downloadUrl=safe_get(version, 'downloadUrl'),
            trainedWords=safe_get(version, 'trainedWords'),
            baseModel=safe_get(version, 'baseModel'),
            files=[ModelVersionFile(
                name=safe_get(f, 'name'),
                id=safe_get(f, 'id'),
                sizeKb=safe_get(f, 'sizeKb'),
                type=safe_get(f, 'type'),
                format=safe_get(f, 'format'),
                pickleScanResult=safe_get(f, 'pickleScanResult'),
                pickleScanMessage=safe_get(f, 'pickleScanMessage'),
                virusScanResult=safe_get(f, 'virusScanResult'),
                scannedAt=parse_datetime(safe_get(f, 'scannedAt')) if safe_get(f, 'scannedAt') else None,
                hashes=safe_get(f, 'hashes'),
                downloadUrl=safe_get(f, 'downloadUrl')
            ) for f in safe_get(version, 'files')],
            images=[ModelVersionImage(
                url=safe_get(i, 'url'),
                nsfw=safe_get(i, 'nsfw'),
                width=safe_get(i, 'width'),
                height=safe_get(i, 'height'),
                hash=safe_get(i, 'hash'),
                meta=safe_get(i, 'meta')
            ) for i in safe_get(version, 'images')],
            stats=ModelVersionStats(
                downloadCount=safe_get(version.get('stats', {}), 'downloadCount'),
                ratingCount=safe_get(version.get('stats', {}), 'ratingCount'),
                rating=safe_get(version.get('stats', {}), 'rating')
            )
        )