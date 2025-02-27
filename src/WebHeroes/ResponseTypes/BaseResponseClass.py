"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass


@dataclass
class BaseResponseClass:
    """
    Base class for all API response data structures.

    Attributes:
        object_type (str): The type of response.
    """

    object_type: str
