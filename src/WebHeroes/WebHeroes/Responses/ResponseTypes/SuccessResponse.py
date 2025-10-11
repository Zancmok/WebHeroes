from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class SuccessResponse(BaseResponseModel):
    object_type: str = field(default="success-response", kw_only=True)
