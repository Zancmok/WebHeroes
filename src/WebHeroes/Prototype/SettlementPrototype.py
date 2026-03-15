from .AbstractBuildingPrototype import AbstractBuildingPrototype


class SettlementPrototype(AbstractBuildingPrototype):
    def __init__(self, name: str, display_name: str, sprite: str, point_value: int, resource_multiplier: int) -> None:
        super().__init__(name, display_name, sprite)

        self.point_value: int = point_value
        self.resource_multiplier: int = resource_multiplier
