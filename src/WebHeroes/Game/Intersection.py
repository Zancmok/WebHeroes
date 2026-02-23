from typing import Optional
from .Settlement import SettlementType
from .Field import Field


class Intersection:
    def __init__(self, fields: list[Field]) -> None:
        self.fields: list[Field] = fields
        self.settlement: Optional[SettlementType] = None
