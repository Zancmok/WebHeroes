"""
This module defines the EmptyResponse class, which represents an empty response with no
additional data. It extends from the `BaseResponseClass` to maintain a consistent response
structure in the API.

Classes:
    EmptyResponse: A response indicating that no additional data is included.
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseResponseModel import BaseResponseModel


@dataclass
class EmptyResponse(BaseResponseModel):
    """
    Represents an empty response with no additional data.

    This class inherits from `BaseResponseClass` and overrides the `object_type`
    attribute to indicate that the response contains no data. It is typically used
    when an API response is required but no further information is necessary.

    Attributes:
        object_type (str): The type of response, defaulted to "empty" to represent
        an empty response.
    """

    object_type: str = field(default="empty", kw_only=True)
