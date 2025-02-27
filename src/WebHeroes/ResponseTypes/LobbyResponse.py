"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class LobbyResponse(BaseResponseClass):
    """
    Represents a game lobby.

    Attributes:
        room_id (int): The lobby's unique identifier.
        name (str): The name of the lobby.
        owner (User): The owner of the lobby.
        members (list[User]): List of users in the lobby.
    """

    object_type: str = field(default="lobby", kw_only=True)

    room_id: int
    name: str
    owner: UserResponse
    members: list[UserResponse]
