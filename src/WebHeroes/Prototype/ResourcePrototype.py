from .AbstractDecalPrototype import AbstractDecalPrototype


class ResourcePrototype(AbstractDecalPrototype):
    def __init__(self, name: str, display_name: str, sprite: str) -> None:
        super().__init__(name, display_name, sprite)
