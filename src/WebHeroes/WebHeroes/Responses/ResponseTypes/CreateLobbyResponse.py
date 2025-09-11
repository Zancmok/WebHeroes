"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.LobbyModel import LobbyModel


@dataclass
class CreateLobbyResponse(BaseResponseModel):
    """
    # TODO: Write Docstring!
    """

    object_type: str = field(default="create-lobby-response", kw_only=True)

    lobby: LobbyModel
