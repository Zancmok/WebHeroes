from LuaBridge import BasePrototype


class PlayerColorType(BasePrototype):
    def __init__(self, name: str, display_name: str, r: int, g: int, b: int) -> None:
        super().__init__(name, display_name)

        self.r: int = r
        self.g: int = g
        self.b: int = b
