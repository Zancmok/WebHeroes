"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class UserLeftUpdateResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    object_type: str = field(default="user-left-update", kw_only=True)

    user: UserResponse
