from LuaBridge import BasePrototype


class SettlementType(BasePrototype):
    def __init__(self, name: str, display_name: str, point_value: int, resource_multiplier: int) -> None:
        super().__init__(name, display_name)

        self.point_value: int = point_value
        self.resource_multiplier: int = resource_multiplier
