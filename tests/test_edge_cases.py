from unittest.mock import patch

import pytest

from civitai_api.civitai_api.api.creators import CreatorsAPI
from civitai_api.civitai_api.api.images import ImagesAPI
from civitai_api.civitai_api.api.model_versions import ModelVersionsAPI
from civitai_api.civitai_api.api.models import ModelsAPI
from civitai_api.civitai_api.api.tags import TagsAPI
from civitai_api.civitai_api.models import Creator, Image, Model, ModelVersion, Tag
from civitai_api.civitai_api.utils import parse_response, safe_get

# Edge case: empty API response


def test_modelsapi_list_models_empty():
    api = ModelsAPI()
    mock_response = {"items": [], "metadata": {}}
    with patch.object(api, "session") as mock_session:
        mock_session.get.return_value.json.return_value = mock_response
        mock_session.get.return_value.raise_for_status.return_value = None
        models = next(api.list_models())
        assert models == []


def test_imagesapi_list_images_empty():
    api = ImagesAPI()
    mock_response = {"items": [], "metadata": {}}
    with patch.object(api, "get", return_value=mock_response):
        images = api.list_images()
        assert images == []


def test_creatorsapi_list_creators_empty():
    api = CreatorsAPI()
    mock_response = {"items": []}
    with patch.object(api, "get", return_value=mock_response):
        creators = api.list_creators()
        assert creators == []


def test_tagsapi_list_tags_empty():
    api = TagsAPI()
    mock_response = {"items": []}
    with patch.object(api, "get", return_value=mock_response):
        tags = api.list_tags()
        assert tags == []


def test_modelversionsapi_get_model_version_missing_fields():
    api = ModelVersionsAPI()
    mock_response = {"id": 1}  # missing most fields
    with patch.object(api, "get", return_value=mock_response):
        with patch.object(api._models_api, "_parse_model_version") as mock_parse:
            mock_parse.return_value = ModelVersion(
                id=1,
                modelId=None,
                name=None,
                createdAt=None,
                downloadUrl=None,
                trainedWords=None,
                baseModel=None,
                files=None,
                images=None,
                stats=None,
            )
            version = api.get_model_version(1)
            assert version.id == 1
            assert version.name is None


# Edge case: safe_get with unexpected types
def test_safe_get_non_dict():
    with pytest.raises(AttributeError):
        safe_get(123, "key")


def test_parse_response_missing_metadata():
    resp = {"items": [1, 2, 3]}
    out = parse_response(resp.copy())
    assert "metadata" not in out
