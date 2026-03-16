from typing import override, Any
from .AbstractBasePrototype import AbstractBasePrototype


class SettingsPrototype(AbstractBasePrototype):
    def __init__(self, name: str, display_name: str, map_size: int) -> None:
        super().__init__(name, display_name)
        self.object_type = "settings-prototype"

        self.map_size: int = map_size

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "map_size": self.map_size
        }
