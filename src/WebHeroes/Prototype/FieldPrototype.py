from typing import Optional, override, Any
from .AbstractDecalPrototype import AbstractDecalPrototype


class FieldPrototype(AbstractDecalPrototype):
    def __init__(self, name: str, display_name: str, sprite: str, weight: int, minimum_amount: int, resource: Optional[str] = None) -> None:
        super().__init__(name, display_name, sprite)
        self.object_type = "field-prototype"

        self.weight: int = weight
        self.minimum_amount: int = minimum_amount
        self.resource: Optional[str] = resource

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "weight": self.weight,
            "minimum_amount": self.minimum_amount,
            "resource": self.resource
        }
