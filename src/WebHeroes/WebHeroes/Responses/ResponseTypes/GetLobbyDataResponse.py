"""
This module defines the GetLobbyDataResponse class, which represents a response containing
data about available lobbies and users. It extends from `BaseResponseClass` to maintain a
consistent response structure.

Classes:
    GetLobbyDataResponse: A response containing information about the requesting user,
    active users, and available lobbies.
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.LobbyModel import LobbyModel
from WebHeroes.Responses.DataModels.UserModel import UserModel


@dataclass
class GetLobbyDataResponse(BaseResponseModel):
    """
    Response containing data about available lobbies and users.

    This response object provides information about the requesting user, a list of active
    users in the system, and a list of available lobbies. It is used when querying for
    lobby-related data.

    Attributes:
        object_type (str): The type of response, set to "get-lobby-data-response" to
        represent this specific response type.
        self (UserModel): The requesting user, represented by a `UserResponse` object.
        users (list[UserResponse]): A list of active users in the system, each represented
        by a `UserResponse` object.
        lobbies (list[LobbyModel]): A list of available lobbies, each represented by
        a `LobbyResponse` object.
    """

    object_type: str = field(default="get-lobby-data-response", kw_only=True)

    self: UserModel
    users: list[UserModel]
    lobbies: list[LobbyModel]
