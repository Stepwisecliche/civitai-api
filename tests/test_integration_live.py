"""Environment-based integration testing.

This approach allows running tests against real API when needed,
while using mocks by default.
"""

import os

import pytest

from civitai_api import Civitai

# Skip integration tests by default unless explicitly enabled
pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Integration tests disabled. Set RUN_INTEGRATION_TESTS=1 to enable.",
)


@pytest.fixture
def civitai_client():
    """Create Civitai client for integration tests."""
    api_key = os.getenv("CIVITAI_API_KEY")
    # API key is optional for read-only operations
    return Civitai(api_key=api_key)


@pytest.mark.integration
def test_list_models_integration(civitai_client):
    """Test listing models with real API."""
    try:
        models_generator = civitai_client.models.list_models(limit=5)
        models = next(models_generator)

        # Basic validation
        assert len(models) <= 5

        for model in models:
            # Verify required fields exist and have expected types
            assert isinstance(model.id, int)
            assert isinstance(model.name, str)
            assert model.name.strip() != ""
            assert model.type is not None
            assert model.creator is not None
            assert isinstance(model.creator.username, str)
            assert model.stats is not None
            assert isinstance(model.stats.downloadCount, int)

    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")


@pytest.mark.integration
def test_get_specific_model_integration(civitai_client):
    """Test getting a specific well-known model."""
    # Use a known stable model ID (Stable Diffusion 1.5)
    model_id = 4201  # Popular model that should always exist

    try:
        model = civitai_client.models.get_model(model_id)

        assert model.id == model_id
        assert isinstance(model.name, str)
        assert len(model.name) > 0
        assert model.description is not None
        assert len(model.modelVersions) > 0

        # Test nested structures
        version = model.modelVersions[0]
        assert version.id is not None
        assert isinstance(version.downloadUrl, str)

        if version.files:
            file = version.files[0]
            assert file.id is not None
            assert isinstance(file.sizeKb, (int, float))
            assert file.downloadUrl is not None

    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")


@pytest.mark.integration
def test_list_images_integration(civitai_client):
    """Test listing images with real API."""
    try:
        images = civitai_client.images.list_images(limit=3, nsfw=False)

        assert len(images) <= 3

        for image in images:
            assert isinstance(image.id, int)
            assert isinstance(image.url, str)
            assert image.url.startswith("http")
            assert isinstance(image.width, int)
            assert isinstance(image.height, int)
            assert image.width > 0
            assert image.height > 0
            assert image.stats is not None

    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")


@pytest.mark.integration
def test_api_error_handling_integration(civitai_client):
    """Test that API errors are handled correctly."""
    from civitai_api import CivitaiAPIError

    # Try to get a non-existent model
    with pytest.raises(CivitaiAPIError):
        civitai_client.models.get_model(99999999)  # Very unlikely to exist
