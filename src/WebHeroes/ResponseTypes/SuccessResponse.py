"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass


@dataclass
class SuccessResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    object_type: str = field(default="success", kw_only=True)
