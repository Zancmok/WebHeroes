from Game.Player import Player
from Prototype import SettlementPrototype
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class SettlementModel(BaseDataModel):
    object_type: str = field(default="settlement-model", kw_only=True)

    settlement_type: SettlementPrototype
    owner: Player
