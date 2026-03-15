from typing import Optional

from .AbstractDecalPrototype import AbstractDecalPrototype


class FieldPrototype(AbstractDecalPrototype):
    def __init__(self, name: str, display_name: str, sprite: str, weight: int, minimum_amount: int, resource: Optional[str] = None) -> None:
        super().__init__(name, display_name, sprite)

        self.weight: int = weight
        self.minimum_amount: int = minimum_amount
        self.resource: Optional[str] = resource
