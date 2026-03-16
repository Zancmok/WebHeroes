from typing import override, Any
from .AbstractDecalPrototype import AbstractDecalPrototype


class AbstractBuildingPrototype(AbstractDecalPrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name, sprite)
        self.object_type = "abstract-building-prototype"

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
        }
