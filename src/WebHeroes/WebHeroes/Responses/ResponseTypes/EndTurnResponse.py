from Game.Player import Player
from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass


@dataclass
class EndTurnResponse(BaseResponseModel):
    object_type: str = field(default="end-turn-response", kw_only=True)

    rolled_number: int
    next_user_index: int
    players: list[Player]
