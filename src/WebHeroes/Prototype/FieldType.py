from typing import Optional

from LuaBridge import BasePrototype
from .ResourceType import ResourceType


class FieldType(BasePrototype):
    def __init__(self, name: str, display_name: str, sprite: str, resource: Optional[str] = None) -> None:
        super().__init__(name, display_name)

        self.resource: Optional[ResourceType] = resource
        self.sprite: str = sprite

        print(self.resource, flush=True)
