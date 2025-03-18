"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseResponseModel import BaseResponseModel


@dataclass
class SuccessResponse(BaseResponseModel):
    """
    # TODO: Write Docstring!
    """

    object_type: str = field(default="success", kw_only=True)
