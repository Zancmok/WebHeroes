from LuaBridge import BasePrototype
from .ResourceType import ResourceType


class Ingredient(BasePrototype):
    def __init__(self, resource: ResourceType, amount: int) -> None:
        super().__init__(f"r_{resource.name}", resource.display_name)

        self.resource: ResourceType = resource
        self.amount: int = amount
