from WebHeroes.Responses.BaseResponseModel import BaseResponseModel

class SignupResponse(BaseResponseModel):
    object_type: str = "signup-response"

    success: bool
    reason: str
