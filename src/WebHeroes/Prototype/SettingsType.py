from LuaBridge import BasePrototype


class SettingsType(BasePrototype):
    def __init__(self, name: str, display_name: str, map_size: int) -> None:
        super().__init__(name, display_name)

        self.map_size: int = map_size
