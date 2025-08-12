"""Defines the Tag dataclass for representing tag information in the Civitai API models."""

from dataclasses import dataclass


@dataclass
class Tag:
    """Represents a tag in the Civitai API.

    Attributes:
        name (str): The name of the tag.
        modelCount (int): The number of models associated with the tag.
        link (str): The URL link to the tag.

    """

    name: str
    modelCount: int
    link: str
