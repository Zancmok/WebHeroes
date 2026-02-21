from typing import Optional

from LuaBridge import BasePrototype
from .ResourceType import ResourceType


class FieldType(BasePrototype):
    def __init__(self, name: str, display_name: str, resource: Optional[str] = None) -> None:
        super().__init__(name, display_name)

        self.resource: Optional[ResourceType] = resource

        print(self.resource, flush=True)
