"""Defines the Creator dataclass representing a model creator with username, model count, and link."""

from dataclasses import dataclass


@dataclass
class Creator:
    """Represents a model creator with username, model count, and link."""

    username: str
    modelCount: int
    link: str
