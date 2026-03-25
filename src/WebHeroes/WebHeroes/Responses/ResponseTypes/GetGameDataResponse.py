from Game.Player import Player
from Prototype.AbstractBasePrototype import AbstractBasePrototype
from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from WebHeroes.Responses.DataModels.FieldModel import FieldModel
from WebHeroes.Responses.DataModels.SettlementModel import SettlementModel
from WebHeroes.Responses.DataModels.RoadModel import RoadModel
from dataclasses import field, dataclass


@dataclass
class GetGameDataResponse(BaseResponseModel):
    object_type: str = field(default="get-game-data-response", kw_only=True)

    fields: dict[str, FieldModel]
    prototypes: list[AbstractBasePrototype]
    players: list[Player]
    settlements: dict[str, SettlementModel]
    roads: dict[str, RoadModel]
    current_user_index: int
    my_index: int
