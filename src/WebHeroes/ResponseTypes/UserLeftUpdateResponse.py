"""
This module defines the UserLeftUpdateResponse class, which represents a notification
about a user leaving the system or a specific lobby. It extends from `BaseResponseClass`
to maintain consistency across response types.

Classes:
    UserLeftUpdateResponse: A response indicating that a user has left the system or lobby.
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class UserLeftUpdateResponse(BaseResponseClass):
    """
    Notification about a user leaving.

    This class represents a response notifying that a user has left the system or a specific
    lobby. It includes the details of the user who has left in the `user` attribute.

    Attributes:
        object_type (str): The type of response, set to "user-left-update" to indicate that
        the response represents a user leaving.
        user (UserResponse): The details of the user who has left, represented by a `UserResponse` object.
    """

    object_type: str = field(default="user-left-update", kw_only=True)

    user: UserResponse
