from .Player import Player
from Prototype import SettlementPrototype


class Settlement:
    def __init__(self, settlement_type: SettlementPrototype, owner: Player) -> None:
        self.settlement_type: SettlementPrototype = settlement_type
        self.owner: Player = owner
