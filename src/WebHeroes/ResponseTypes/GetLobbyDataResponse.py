"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse
from WebHeroes.ResponseTypes.LobbyResponse import LobbyResponse


@dataclass
class GetLobbyDataResponse(BaseResponseClass):
    """
    Response containing data about available lobbies and users.

    Attributes:
        self (UserResponse): The requesting user.
        users (list[UserResponse]): List of active users.
        lobbies (list[LobbyResponse]): List of available lobbies.
    """

    response_type: str = field(default="get-lobby-data-response", kw_only=True)

    self: UserResponse
    users: list[UserResponse]
    lobbies: list[LobbyResponse]
