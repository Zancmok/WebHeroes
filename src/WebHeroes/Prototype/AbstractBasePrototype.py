from typing import override, Any
from LuaBridge import BasePrototype
from WebHeroes.Responses.AlternateDataModel import AlternateDataModel


class AbstractBasePrototype(BasePrototype, AlternateDataModel):
    def __init__(self, name: str, display_name: str) -> None:
        super().__init__(name, display_name)
        self.object_type = "abstract-base-prototype"

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "name": self.name,
            "display_name": self.display_name
        }
