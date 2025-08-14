"""Unit tests for civitai_api package APIs.

This module contains tests for ModelsAPI, ImagesAPI, CreatorsAPI, TagsAPI, and ModelVersionsAPI,
including parsing and error handling.
"""

from unittest.mock import MagicMock, patch

import pytest

from civitai_api.civitai_api.api.creators import CreatorsAPI
from civitai_api.civitai_api.api.images import ImagePeriod, ImagesAPI, ImageSort
from civitai_api.civitai_api.api.model_versions import ModelVersionsAPI
from civitai_api.civitai_api.api.models import (
    CommercialUse,
    ModelCategory,
    ModelPeriod,
    ModelsAPI,
    ModelSort,
)
from civitai_api.civitai_api.api.tags import TagsAPI
from civitai_api.civitai_api.models import Creator, Image, Model, ModelVersion, Tag


# ModelsAPI tests
def test_modelsapi_list_models_parsing():
    api = ModelsAPI()
    mock_response = {
        "items": [
            {
                "id": 1,
                "name": "Test Model",
                "description": "desc",
                "type": "Checkpoint",
                "nsfw": False,
                "tags": ["tag1"],
                "mode": None,
                "creator": {"username": "user", "image": None},
                "stats": {
                    "downloadCount": 1,
                    "favoriteCount": 2,
                    "commentCount": 3,
                    "ratingCount": 4,
                    "rating": 5.0,
                },
                "modelVersions": [],
            }
        ],
        "metadata": {"nextPage": None},
    }
    with patch.object(api, "session") as mock_session:
        mock_session.get.return_value.json.return_value = mock_response
        mock_session.get.return_value.raise_for_status.return_value = None
        models = next(api.list_models())
        assert isinstance(models[0], Model)
        assert models[0].name == "Test Model"


# ImagesAPI tests
def test_imagesapi_list_images_parsing():
    api = ImagesAPI()
    mock_response = {
        "items": [
            {
                "id": 1,
                "url": "http://img",
                "hash": "abc",
                "width": 100,
                "height": 200,
                "nsfw": False,
                "createdAt": "2025-08-14T12:34:56",
                "postId": 2,
                "stats": {
                    "cryCount": 0,
                    "laughCount": 1,
                    "likeCount": 2,
                    "heartCount": 3,
                    "commentCount": 4,
                },
                "meta": {},
                "username": "user",
            }
        ],
        "metadata": {},
    }
    with patch.object(api, "get", return_value=mock_response):
        images = api.list_images()
        assert isinstance(images[0], Image)
        assert images[0].url == "http://img"


# CreatorsAPI tests
def test_creatorsapi_list_creators_parsing():
    api = CreatorsAPI()
    mock_response = {
        "items": [{"username": "user", "modelCount": 5, "link": "http://link"}]
    }
    with patch.object(api, "get", return_value=mock_response):
        creators = api.list_creators()
        assert isinstance(creators[0], Creator)
        assert creators[0].username == "user"
        assert creators[0].modelCount == 5


# TagsAPI tests
def test_tagsapi_list_tags_parsing():
    api = TagsAPI()
    mock_response = {"items": [{"name": "tag", "modelCount": 10, "link": "http://tag"}]}
    with patch.object(api, "get", return_value=mock_response):
        tags = api.list_tags()
        assert isinstance(tags[0], Tag)
        assert tags[0].name == "tag"
        assert tags[0].modelCount == 10


# ModelVersionsAPI tests
def test_modelversionsapi_get_model_version_parsing():
    api = ModelVersionsAPI()
    mock_response = {
        "id": 1,
        "modelId": 2,
        "name": "ver",
        "createdAt": "2025-08-14T12:34:56",
        "downloadUrl": "http://dl",
        "trainedWords": ["word"],
        "baseModel": "SD 1.5",
        "files": [],
        "images": [],
        "stats": {"downloadCount": 1, "ratingCount": 2, "rating": 3.0},
    }
    with patch.object(api, "get", return_value=mock_response):
        with patch.object(api._models_api, "_parse_model_version") as mock_parse:
            mock_parse.return_value = ModelVersion(
                id=1,
                modelId=2,
                name="ver",
                createdAt=None,
                downloadUrl="http://dl",
                trainedWords=["word"],
                baseModel="SD 1.5",
                files=[],
                images=[],
                stats=None,
            )
            version = api.get_model_version(1)
            assert isinstance(version, ModelVersion)
            assert version.name == "ver"


# Error handling tests
def test_modelsapi_get_model_error():
    api = ModelsAPI()
    with patch.object(api, "get", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            api.get_model(1)


def test_imagesapi_list_images_error():
    api = ImagesAPI()
    with patch.object(api, "get", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            api.list_images()


def test_creatorsapi_list_creators_error():
    api = CreatorsAPI()
    with patch.object(api, "get", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            api.list_creators()


def test_tagsapi_list_tags_error():
    api = TagsAPI()
    with patch.object(api, "get", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            api.list_tags()


def test_modelversionsapi_get_model_version_error():
    api = ModelVersionsAPI()
    with patch.object(api, "get", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            api.get_model_version(1)
