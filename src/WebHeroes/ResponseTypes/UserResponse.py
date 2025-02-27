"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.PresenceStatus import PresenceStatus


@dataclass
class UserResponse(BaseResponseClass):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The user's unique identifier.
        username (str): The user's name.
        avatar_url (str): The URL to the user's avatar.
        presence_status (PresenceStatus): The user's online presence status.
    """

    object_type: str = field(default="user", kw_only=True)

    user_id: int
    username: str
    avatar_url: str
    presence_status: PresenceStatus
