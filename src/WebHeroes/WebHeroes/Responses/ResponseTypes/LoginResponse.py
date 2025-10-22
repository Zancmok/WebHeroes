from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class LoginResponse(BaseResponseModel):
    object_type: str = field(default="login-response", kw_only=True)

    token: str
