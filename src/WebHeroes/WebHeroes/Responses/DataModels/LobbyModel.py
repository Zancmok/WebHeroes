"""
This module defines the LobbyResponse class, which represents a game lobby response
containing details about the lobby, its owner, and its members. It extends from
`BaseResponseClass` to maintain a consistent structure for response objects.

Classes:
    LobbyResponse: A response containing information about a specific game lobby,
    including its unique ID, name, owner, and members.
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseDataModel import BaseDataModel
from WebHeroes.Responses.DataModels.UserModel import UserModel


@dataclass
class LobbyModel(BaseDataModel):
    """
    Represents a game lobby.

    This class provides details about a game lobby, such as the unique room ID, the
    name of the lobby, the owner of the lobby, and the list of members currently in the lobby.

    Attributes:
        object_type (str): The type of response, set to "lobby" to represent this specific
        response type.
        room_id (int): The unique identifier for the lobby.
        name (str): The name of the lobby.
        owner (UserModel): The user who owns the lobby, represented by a `UserResponse` object.
        members (list[UserResponse]): A list of users in the lobby, each represented by a
        `UserResponse` object.
    """

    object_type: str = field(default="lobby", kw_only=True)

    room_id: int
    name: str
    owner: UserModel
    members: list[UserModel]
