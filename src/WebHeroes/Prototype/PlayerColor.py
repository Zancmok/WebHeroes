from typing import override, Any
from .AbstractBasePrototype import AbstractBasePrototype


class PlayerColor(AbstractBasePrototype):
    def __init__(self, name: str, display_name: str, r: int, g: int, b: int) -> None:
        super().__init__(name, display_name)
        self.object_type = "player-color-prototype"

        self.r: int = r
        self.g: int = g
        self.b: int = b

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "r": self.r,
            "g": self.g,
            "b": self.b
        }
