from typing import Optional

from LuaBridge import BasePrototype
from .ResourceType import ResourceType


class FieldType(BasePrototype):
    def __init__(self, name: str, display_name: str, sprite: str, weight: int, minimum_amount: int, resource: Optional[ResourceType] = None) -> None:
        super().__init__(name, display_name)

        self.resource: Optional[ResourceType] = resource
        self.sprite: str = sprite
        self.weight: int = weight
        self.minimum_amount: int = minimum_amount
