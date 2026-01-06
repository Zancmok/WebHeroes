from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class MemberModel(BaseResponseModel):
    object_type: str = field(default="member-model", kw_only=True)

    member_id: int
    member_name: str
