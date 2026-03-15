from LuaBridge import BasePrototype


class AbstractDecalPrototype(BasePrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name)

        self.sprite: str = sprite
