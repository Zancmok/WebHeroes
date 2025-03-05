"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.LobbyUpdate import LobbyUpdate
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.NewUserUpdateResponse import NewUserUpdateResponse
from WebHeroes.ResponseTypes.NewLobbyUpdateResponse import NewLobbyUpdateResponse
from WebHeroes.ResponseTypes.UserUpdatedUpdateResponse import UserUpdatedUpdateResponse
from WebHeroes.ResponseTypes.UserLeftUpdateResponse import UserLeftUpdateResponse


@dataclass
class LobbyUpdateResponse(BaseResponseClass):
    """
    Response containing an update about a lobby.

    Attributes:
        change_type (LobbyUpdate): The type of change that occurred.
        change (NewUserUpdateResponse | NewLobbyUpdateResponse | UserUpdatedUpdateResponse): Details of the change.
    """

    object_type: str = field(default="lobby-update", kw_only=True)
    change_type: LobbyUpdate
    change: NewUserUpdateResponse | NewLobbyUpdateResponse | UserUpdatedUpdateResponse | UserLeftUpdateResponse
