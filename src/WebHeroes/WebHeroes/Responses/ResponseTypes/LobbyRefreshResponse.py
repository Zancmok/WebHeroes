from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from WebHeroes.Responses.DataModels.LobbyModel import LobbyModel
from dataclasses import field, dataclass


@dataclass
class LobbyRefreshResponse(BaseResponseModel):
    object_type: str = field(default="lobby-refresh-response", kw_only=True)

    members: list[MemberModel]
    lobbies: list[LobbyModel]
