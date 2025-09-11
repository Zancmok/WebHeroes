"""
This module defines the UserResponse class, which represents a user in the system.
It contains essential information about the user, including their ID, username, avatar,
and presence status.

Classes:
    UserResponse: A response containing information about a user in the system.
"""

from dataclasses import dataclass, field

from Enums.Common.PresenceStatus import PresenceStatus
from WebHeroes.Responses.BaseDataModel import BaseDataModel


@dataclass
class UserModel(BaseDataModel):
    """
    Represents a user in the system.

    This class contains details about a user, such as their unique identifier, username,
    avatar URL, and current online presence status. It is used to represent a user object
    in the system's responses.

    Attributes:
        object_type (str): The type of response, set to "user" to represent this specific
        response type.
        user_id (int): The unique identifier for the user.
        username (str): The username of the user.
        avatar_url (str): The URL to the user's avatar image.
        presence_status (PresenceStatus): The current online status of the user, represented
        by a `PresenceStatus` enumeration.
    """

    object_type: str = field(default="user", kw_only=True)

    user_id: int
    username: str
    avatar_url: str
    presence_status: PresenceStatus
