from LuaBridge import BasePrototype


class Ingredient(BasePrototype):
    def __init__(self, resource: str, amount: int) -> None:
        super().__init__(f"r_{resource}", resource)

        self.resource: str = resource
        self.amount: int = amount
