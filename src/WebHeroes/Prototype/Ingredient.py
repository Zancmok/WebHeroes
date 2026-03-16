from typing import Any, override
from .AbstractBasePrototype import AbstractBasePrototype


class Ingredient(AbstractBasePrototype):
    def __init__(self, resource: str, amount: int) -> None:
        super().__init__(f"r_{resource}", resource)
        self.object_type = "ingredient-s_prototype"

        self.resource: str = resource
        self.amount: int = amount

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "resource": self.resource,
            "amount": self.amount
        }
