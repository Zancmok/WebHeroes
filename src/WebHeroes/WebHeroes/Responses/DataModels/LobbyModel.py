from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from dataclasses import field, dataclass


@dataclass
class LobbyModel(BaseResponseModel):
    object_type: str = field(default="lobby-model", kw_only=True)

    lobby_name: str
    owner_id: int
    members: list[MemberModel]
