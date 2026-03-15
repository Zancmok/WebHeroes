from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.MapModel import MapModel
from WebHeroes.Responses.DataModels.RecipeModel import RecipeModel
from dataclasses import field, dataclass


@dataclass
class GetGameDataResponse(BaseResponseModel):
    object_type: str = field(default="get-game-data-response", kw_only=True)

    map: MapModel
    recipes: list[RecipeModel]
