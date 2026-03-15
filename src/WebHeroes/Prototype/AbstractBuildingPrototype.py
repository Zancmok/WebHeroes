from .AbstractDecalPrototype import AbstractDecalPrototype


class AbstractBuildingPrototype(AbstractDecalPrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name, sprite)
