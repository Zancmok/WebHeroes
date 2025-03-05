"""
This module defines the GetLobbyDataResponse class, which represents a response containing
data about available lobbies and users. It extends from `BaseResponseClass` to maintain a
consistent response structure.

Classes:
    GetLobbyDataResponse: A response containing information about the requesting user,
    active users, and available lobbies.
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.LobbyResponse import LobbyResponse
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class GetLobbyDataResponse(BaseResponseClass):
    """
    Response containing data about available lobbies and users.

    This response object provides information about the requesting user, a list of active
    users in the system, and a list of available lobbies. It is used when querying for
    lobby-related data.

    Attributes:
        object_type (str): The type of response, set to "get-lobby-data-response" to
        represent this specific response type.
        self (UserResponse): The requesting user, represented by a `UserResponse` object.
        users (list[UserResponse]): A list of active users in the system, each represented
        by a `UserResponse` object.
        lobbies (list[LobbyResponse]): A list of available lobbies, each represented by
        a `LobbyResponse` object.
    """

    object_type: str = field(default="get-lobby-data-response", kw_only=True)

    self: UserResponse
    users: list[UserResponse]
    lobbies: list[LobbyResponse]
