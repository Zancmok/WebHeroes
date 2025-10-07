from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class SignupResponse(BaseResponseModel):
    object_type: str = field(default="signup-response", kw_only=True)

    success: bool
    reason: str
