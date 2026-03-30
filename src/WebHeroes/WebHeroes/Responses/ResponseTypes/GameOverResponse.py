from WebHeroes.Responses.BaseResponseModel import BaseResponseModel
from dataclasses import field, dataclass
from Game.Player import Player


@dataclass
class GameOverResponse(BaseResponseModel):
    object_type: str = field(default="game-over-response", kw_only=True)

    winner: Player
