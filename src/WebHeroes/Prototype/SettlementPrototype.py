from typing import Any, override, Optional
from .AbstractBuildingPrototype import AbstractBuildingPrototype


class SettlementPrototype(AbstractBuildingPrototype):
    def __init__(self, name: str, display_name: str, sprite: str, point_value: int, resource_multiplier: int, prerequisite_building: Optional[str] = None) -> None:
        super().__init__(name, display_name, sprite)
        self.object_type = "settlement-prototype"

        self.point_value: int = point_value
        self.resource_multiplier: int = resource_multiplier
        self.prerequisite_building: Optional[str] = prerequisite_building

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "point_value": self.point_value,
            "resource_multiplier": self.resource_multiplier,
            "prerequisite_building": self.prerequisite_building
        }
