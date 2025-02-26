"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass


@dataclass
class BaseResponseClass:
    """
    Base class for all API response data structures.

    Attributes:
        response_type (str): The type of response.
    """

    response_type: str
