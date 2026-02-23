from .Player import Player
from Prototype import SettlementType


class Settlement:
    def __init__(self, settlement_type: SettlementType, owner: Player) -> None:
        self.settlement_type: SettlementType = settlement_type
        self.owner: Player = owner
