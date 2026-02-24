from typing import Optional
from .Settlement import SettlementType


class Intersection:
    def __init__(self) -> None:
        self.settlement: Optional[SettlementType] = None
