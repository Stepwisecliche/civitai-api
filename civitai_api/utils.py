"""Utility functions for parsing datetimes, API responses, enums, and safely accessing dictionary keys."""

from datetime import datetime
from enum import Enum
from typing import Any


def parse_datetime(dt_str: str) -> datetime:
    """Parse an ISO 8601 datetime string with a compatability shim for earlier versions of Python.

    Args:
        dt_str (str): The datetime string to parse.

    Returns:
        datetime: A datetime object parsed from the input string.

    """
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        if dt_str.endswith("Z"):
            return datetime.fromisoformat(dt_str[:-1] + "+00:00")  # noqa: FURB162
        raise


def parse_response(response: dict[str, Any]) -> dict[str, Any]:
    """Parse common response fields."""
    if "metadata" in response:
        response["metadata"] = {
            "totalItems": response["metadata"].get("totalItems"),
            "currentPage": response["metadata"].get("currentPage"),
            "pageSize": response["metadata"].get("pageSize"),
            "totalPages": response["metadata"].get("totalPages"),
            "nextPage": response["metadata"].get("nextPage"),
            "prevPage": response["metadata"].get("prevPage"),
        }
    return response


def create_enum_list(enum_class: type[Enum], values: list[str]) -> list[Any]:
    """Create a list of enum instances from a list of string values.

    Args:
        enum_class (type[Enum]): The enum class to instantiate.
        values (list[str]): List of string values to convert to enum instances.

    Returns:
        list[Any]: List of enum instances corresponding to the input values.

    """
    return [enum_class(value) for value in values]


def safe_get(d: dict, key: str) -> str | int | bool | None:
    """Safely get the value for a key from a dictionary, returning None if the key is not present.

    tbh, this function seems like an unnecessary middleman.

    Args:
        d (dict): The dictionary to access.
        key (str): The key to look up.

    Returns:
        str: The value associated with the key, or None if the key is not present.

    """
    return d.get(key)
