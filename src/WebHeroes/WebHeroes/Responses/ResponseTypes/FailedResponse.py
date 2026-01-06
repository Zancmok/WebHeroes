from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class FailedResponse(BaseResponseModel):
    object_type: str = field(default="failed-response", kw_only=True)

    reason: str
