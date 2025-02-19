"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass
from typing import Any
from PresenceStatus import PresenceStatus
from LobbyUpdate import LobbyUpdate


@dataclass
class BaseResponseClass:
    """
    # TODO: Write Docstring!
    """

    type: str


def to_dict(specimen: BaseResponseClass) -> dict[Any, Any]:
    """
    # TODO: Write Docstring!
    :return:
    """


@dataclass
class EmptyResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "empty"


@dataclass
class User(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "user"

    user_id: int
    username: str
    avatar_url: str
    presence_status: PresenceStatus


@dataclass
class Lobby(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "lobby"

    room_id: int
    name: str
    owner: User
    members: list[User]


@dataclass
class GetLobbyDataResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "get-lobby-data-response"

    self: User
    users: list[User]
    lobbies: list[Lobby]


@dataclass
class NewUserUpdate(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "new-user-update"


@dataclass
class NewLobbyUpdate(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "new-lobby-update"


@dataclass
class UserUpdatedUpdate(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "user-updated-update"


@dataclass
class LobbyUpdateResponse(BaseResponseClass):
    """
    # TODO: Write Docstring!
    """

    type = "lobby-update"

    change_type: LobbyUpdate
    change: NewUserUpdate | NewLobbyUpdate | UserUpdatedUpdate
