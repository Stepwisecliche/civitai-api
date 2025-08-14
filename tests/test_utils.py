import pytest
from datetime import datetime
from civitai_api.civitai_api.utils import (
    parse_datetime,
    parse_response,
    create_enum_list,
    safe_get,
)
from enum import Enum


class DummyEnum(Enum):
    A = "A"
    B = "B"


def test_parse_datetime_iso():
    dt = parse_datetime("2025-08-14T12:34:56")
    assert isinstance(dt, datetime)
    assert dt.year == 2025
    assert dt.month == 8
    assert dt.day == 14


def test_parse_datetime_z():
    dt = parse_datetime("2025-08-14T12:34:56Z")
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None


def test_parse_datetime_invalid():
    with pytest.raises(ValueError):
        parse_datetime("not-a-date")


def test_parse_response_metadata():
    resp = {
        "metadata": {
            "totalItems": 1,
            "currentPage": 2,
            "pageSize": 3,
            "totalPages": 4,
            "nextPage": 5,
            "prevPage": 6,
        }
    }
    out = parse_response(resp.copy())
    assert set(out["metadata"].keys()) == {
        "totalItems",
        "currentPage",
        "pageSize",
        "totalPages",
        "nextPage",
        "prevPage",
    }


def test_parse_response_no_metadata():
    resp = {"foo": "bar"}
    out = parse_response(resp.copy())
    assert out["foo"] == "bar"


def test_create_enum_list():
    result = create_enum_list(DummyEnum, ["A", "B"])
    assert result == [DummyEnum.A, DummyEnum.B]


def test_create_enum_list_invalid():
    with pytest.raises(ValueError):
        create_enum_list(DummyEnum, ["C"])


def test_safe_get_present():
    d = {"x": 1}
    assert safe_get(d, "x") == 1


def test_safe_get_missing():
    d = {"x": 1}
    assert safe_get(d, "y") is None
