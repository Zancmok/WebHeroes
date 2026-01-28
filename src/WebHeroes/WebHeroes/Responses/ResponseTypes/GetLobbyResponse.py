from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from dataclasses import field, dataclass


@dataclass
class GetLobbyResponse(BaseResponseModel):
    object_type: str = field(default="get-lobby-response", kw_only=True)

    owner: MemberModel
    members: list[MemberModel]
