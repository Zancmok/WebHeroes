from Game.Player import Player
from Prototype.AbstractBasePrototype import AbstractBasePrototype
from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.FieldModel import FieldModel
from dataclasses import field, dataclass


@dataclass
class GetGameDataResponse(BaseResponseModel):
    object_type: str = field(default="get-game-data-response", kw_only=True)

    fields: dict[str, FieldModel]
    prototypes: list[AbstractBasePrototype]
    players: list[Player]
