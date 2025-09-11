"""
This module defines the BaseResponseClass, which serves as the base class for all API response
data structures.

The BaseResponseClass includes a common attribute `object_type`, which represents the type of
response. This class can be extended by other response classes to add more specific attributes.

Classes:
    BaseResponseClass: The base class for API response data structures, containing common
    attributes for all responses.
"""

from dataclasses import dataclass


@dataclass
class BaseDataModel:
    """
    Base class for all API response data structures.

    This class provides a foundation for response objects, and it includes a common attribute
    `object_type` to specify the type of response. Other response classes can inherit from this
    class to include additional fields relevant to the specific response.

    Attributes:
        object_type (str): The type of response, typically indicating the kind of data the
        response represents.
    """

    object_type: str
