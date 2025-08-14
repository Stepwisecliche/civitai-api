"""Integration tests using recorded real API responses.

This approach records real API responses once and replays them in tests.
Benefits:
- Uses real API data structure
- Fast test execution (no network calls)
- Deterministic results
- No API rate limiting issues
"""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from civitai_api import Civitai
from civitai_api.civitai_api.api.models import ModelsAPI

# Path to store recorded responses
FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)


class ResponseRecorder:
    """Helper to record and replay API responses."""

    def __init__(self, fixture_file: str):
        self.fixture_path = FIXTURES_DIR / f"{fixture_file}.json"
        self.responses = {}
        if self.fixture_path.exists():
            with open(self.fixture_path) as f:
                self.responses = json.load(f)

    def record_response(self, key: str, response_data: dict):
        """Record a response for later replay."""
        self.responses[key] = response_data
        with open(self.fixture_path, "w") as f:
            json.dump(self.responses, f, indent=2, default=str)

    def get_response(self, key: str) -> dict:
        """Get recorded response."""
        return self.responses.get(key)


# Global recorder instance
recorder = ResponseRecorder("api_responses")


def test_models_list_with_real_data():
    """Test model listing with real API response data."""
    response_key = "models_list_page1"

    # Check if we have recorded data
    recorded_response = recorder.get_response(response_key)

    # If no recorded data and RECORD_RESPONSES is set, record it now
    if recorded_response is None:
        if os.getenv("RECORD_RESPONSES") == "1":
            try:
                api = ModelsAPI()
                response = api.session.get(
                    f"{api.BASE_URL}/models", params={"limit": 10}
                )
                response.raise_for_status()
                recorded_response = response.json()
                recorder.record_response(response_key, recorded_response)
                print(f"Recorded response for {response_key}")
            except Exception as e:
                pytest.skip(f"Failed to record response: {e}")
        else:
            pytest.skip(
                "No recorded response available. Run with RECORD_RESPONSES=1 to record."
            )

    api = ModelsAPI()
    with patch.object(api, "session") as mock_session:
        mock_session.get.return_value.json.return_value = recorded_response
        mock_session.get.return_value.raise_for_status.return_value = None

        models = next(api.list_models(limit=10))

        # Verify we got real model data
        assert len(models) > 0
        for model in models:
            assert model.id is not None
            assert model.name is not None
            assert model.type is not None
            assert model.creator is not None
            assert model.stats is not None


def test_model_get_with_real_data():
    """Test individual model retrieval with real API response."""
    response_key = "model_get_1102"

    recorded_response = recorder.get_response(response_key)

    # If no recorded data and RECORD_RESPONSES is set, record it now
    if recorded_response is None:
        if os.getenv("RECORD_RESPONSES") == "1":
            try:
                api = ModelsAPI()
                response = api.session.get(f"{api.BASE_URL}/models/1102")
                response.raise_for_status()
                recorded_response = response.json()
                recorder.record_response(response_key, recorded_response)
                print(f"Recorded response for {response_key}")
            except Exception as e:
                pytest.skip(f"Failed to record response: {e}")
        else:
            pytest.skip(
                "No recorded response available. Run with RECORD_RESPONSES=1 to record."
            )

    api = ModelsAPI()
    with patch.object(api, "get", return_value=recorded_response):
        model = api.get_model(1102)

        # Verify model data structure
        assert model.id == 1102
        assert model.name is not None
        assert model.description is not None
        assert len(model.modelVersions) > 0

        # Test nested objects
        version = model.modelVersions[0]
        assert version.id is not None
        assert version.downloadUrl is not None
        assert len(version.files) > 0


# Helper script to record responses (run separately)
def record_real_responses():
    """Helper to record real API responses. Run this manually when needed."""
    import os

    if os.getenv("RECORD_RESPONSES") != "1":
        return

    api = ModelsAPI()

    # Record models list
    try:
        response = api.session.get(f"{api.BASE_URL}/models", params={"limit": 10})
        response.raise_for_status()
        recorder.record_response("models_list_page1", response.json())
        print("Recorded models list response")
    except Exception as e:
        print(f"Failed to record models list: {e}")

    # Record specific model
    try:
        response = api.session.get(f"{api.BASE_URL}/models/1102")
        response.raise_for_status()
        recorder.record_response("model_get_1102", response.json())
        print("Recorded model 1102 response")
    except Exception as e:
        print(f"Failed to record model 1102: {e}")


if __name__ == "__main__":
    record_real_responses()
