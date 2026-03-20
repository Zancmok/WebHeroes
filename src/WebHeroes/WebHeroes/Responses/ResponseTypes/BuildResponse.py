from Game.Player import Player
from Prototype.AbstractBuildingPrototype import AbstractBuildingPrototype
from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class BuildResponse(BaseResponseModel):
    object_type: str = field(default="build-response", kw_only=True)

    building: AbstractBuildingPrototype
    location: list[int]
    player: Player
