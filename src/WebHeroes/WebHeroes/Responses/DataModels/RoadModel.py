from Game.Player import Player
from Prototype import RoadPrototype
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class RoadModel(BaseDataModel):
    object_type: str = field(default="road-model", kw_only=True)

    road_type: RoadPrototype
    owner: Player
