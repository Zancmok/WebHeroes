"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass


@dataclass
class EmptyResponse(BaseResponseClass):
    """
    Represents an empty response with no additional data.
    """

    response_type: str = field(default="empty", kw_only=True)
