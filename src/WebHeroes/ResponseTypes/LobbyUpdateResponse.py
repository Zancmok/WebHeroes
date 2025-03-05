"""
This module defines the LobbyUpdateResponse class, which represents a response containing
details about an update to a lobby. It extends from `BaseResponseClass` to ensure a consistent
structure for response objects.

Classes:
    LobbyUpdateResponse: A response containing information about a specific update to a lobby,
    including the type of change and the details of the update.
"""

from dataclasses import dataclass, field

from Enums.Server.LobbyUpdate import LobbyUpdate
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.NewLobbyUpdateResponse import NewLobbyUpdateResponse
from WebHeroes.ResponseTypes.NewUserUpdateResponse import NewUserUpdateResponse
from WebHeroes.ResponseTypes.UserLeftUpdateResponse import UserLeftUpdateResponse
from WebHeroes.ResponseTypes.UserUpdatedUpdateResponse import UserUpdatedUpdateResponse


@dataclass
class LobbyUpdateResponse(BaseResponseClass):
    """
    Response containing an update about a lobby.

    This class represents a response indicating a change or update in a lobby. It includes
    information about the type of change (e.g., new user, new lobby, user updated) and the
    specific details of the change.

    Attributes:
        object_type (str): The type of response, set to "lobby-update" to represent this
        specific response type.
        change_type (LobbyUpdate): The type of change that occurred, represented as an
        enumeration from the `LobbyUpdate` enum.
        change (NewUserUpdateResponse | NewLobbyUpdateResponse | UserUpdatedUpdateResponse |
        UserLeftUpdateResponse): The specific details of the change, which can be one of the
        following response types: `NewUserUpdateResponse`, `NewLobbyUpdateResponse`,
        `UserUpdatedUpdateResponse`, or `UserLeftUpdateResponse`.
    """

    object_type: str = field(default="lobby-update", kw_only=True)
    change_type: LobbyUpdate
    change: (NewUserUpdateResponse | NewLobbyUpdateResponse | UserUpdatedUpdateResponse | UserLeftUpdateResponse)
