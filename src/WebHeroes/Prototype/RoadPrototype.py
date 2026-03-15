from .AbstractBuildingPrototype import AbstractBuildingPrototype


class RoadPrototype(AbstractBuildingPrototype):
    def __init__(self, name: str, display_name: str, decal: str) -> None:
        super().__init__(name, display_name, decal)
