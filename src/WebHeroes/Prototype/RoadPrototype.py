from typing import Any, override
from .AbstractBuildingPrototype import AbstractBuildingPrototype


class RoadPrototype(AbstractBuildingPrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name, sprite)
        self.object_type = "road-prototype"

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify()
        }
