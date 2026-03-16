from typing import Any, override
from .AbstractBuildingPrototype import AbstractBuildingPrototype


class RoadPrototype(AbstractBuildingPrototype):
    def __init__(self, name: str, display_name: str, decal: str) -> None:
        super().__init__(name, display_name, decal)
        self.object_type = "road-prototype"

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify()
        }
