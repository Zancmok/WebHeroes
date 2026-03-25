from typing import override, Any
from Prototype import PlayerColor, ResourcePrototype
from WebHeroes.Responses.AlternateDataModel import AlternateDataModel


class Player(AlternateDataModel):
    def __init__(self, color_type: PlayerColor, resource_prototypes: list[ResourcePrototype]) -> None:
        super().__init__()
        self.object_type = "player-s_prototype"

        self.color_type: PlayerColor = color_type

        self.resources: dict[str, int] = {
            resource_prototype.name: 2
            for resource_prototype in resource_prototypes
        }

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "color_type": self.color_type.to_dictify(),
            "resources": self.resources
        }
