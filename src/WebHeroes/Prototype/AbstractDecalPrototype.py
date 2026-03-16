from typing import override, Any
from .AbstractBasePrototype import AbstractBasePrototype


class AbstractDecalPrototype(AbstractBasePrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name)
        self.object_type = "abstract-decal-prototype"

        self.sprite: str = sprite

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "sprite": self.sprite
        }
