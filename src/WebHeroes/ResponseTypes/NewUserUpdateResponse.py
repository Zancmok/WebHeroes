"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class NewUserUpdateResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    object_type: str = field(default="new-user-update", kw_only=True)

    user: UserResponse
