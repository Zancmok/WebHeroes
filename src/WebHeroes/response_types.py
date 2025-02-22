"""
response_types.py

This module defines response data structures and utilities for handling WebHeroes API responses.
"""

from dataclasses import dataclass
from typing import Any
from enum import Enum
from ZancmokLib.dataclass_util import auto_defaults
from WebHeroes.PresenceStatus import PresenceStatus
from WebHeroes.LobbyUpdate import LobbyUpdate


@dataclass
class BaseResponseClass:
    """
    Base class for all API response data structures.

    Attributes:
        response_type (str): The type of response.
    """

    response_type: str


def dictify(data: BaseResponseClass) -> dict[str, Any]:
    """
    Converts a response object into a dictionary, handling nested objects and enums.

    Args:
        data (BaseResponseClass): The response object to convert.

    Returns:
        dict[str, Any]: The dictionary representation of the response object.
    """

    out: dict[str, Any] = {}

    for attribute in dir(data):
        if attribute[:2] == "__":
            continue

        attribute_value: Any = getattr(data, attribute)

        if isinstance(attribute_value, Enum):
            attribute_value = str(attribute_value)
        elif isinstance(attribute_value, BaseResponseClass):
            attribute_value = dictify(attribute_value)

        out[attribute] = attribute_value

    return out


@auto_defaults
@dataclass
class EmptyResponse(BaseResponseClass):
    """
    Represents an empty response with no additional data.
    """

    response_type = "empty"


@auto_defaults
@dataclass
class User(BaseResponseClass):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The user's unique identifier.
        username (str): The user's name.
        avatar_url (str): The URL to the user's avatar.
        presence_status (PresenceStatus): The user's online presence status.
    """

    response_type = "user"

    user_id: int
    username: str
    avatar_url: str
    presence_status: PresenceStatus


@auto_defaults
@dataclass
class Lobby(BaseResponseClass):
    """
    Represents a game lobby.

    Attributes:
        room_id (int): The lobby's unique identifier.
        name (str): The name of the lobby.
        owner (User): The owner of the lobby.
        members (list[User]): List of users in the lobby.
    """

    response_type = "lobby"

    room_id: int
    name: str
    owner: User
    members: list[User]


@auto_defaults
@dataclass
class GetLobbyDataResponse(BaseResponseClass):
    """
    Response containing data about available lobbies and users.

    Attributes:
        self (User): The requesting user.
        users (list[User]): List of active users.
        lobbies (list[Lobby]): List of available lobbies.
    """

    response_type = "get-lobby-data-response"

    self: User
    users: list[User]
    lobbies: list[Lobby]


@auto_defaults
@dataclass
class NewUserUpdate(BaseResponseClass):
    """
    Notification about a new user joining the system.
    """

    response_type = "new-user-update"


@auto_defaults
@dataclass
class NewLobbyUpdate(BaseResponseClass):
    """
    Notification about a new lobby being created.
    """

    response_type = "new-lobby-update"


@auto_defaults
@dataclass
class UserUpdatedUpdate(BaseResponseClass):
    """
    Notification about a user's information being updated.
    """

    response_type = "user-updated-update"


@auto_defaults
@dataclass
class LobbyUpdateResponse(BaseResponseClass):
    """
    Response containing an update about a lobby.

    Attributes:
        change_type (LobbyUpdate): The type of change that occurred.
        change (NewUserUpdate | NewLobbyUpdate | UserUpdatedUpdate): Details of the change.
    """

    response_type = "lobby-update"

    change_type: LobbyUpdate
    change: NewUserUpdate | NewLobbyUpdate | UserUpdatedUpdate
