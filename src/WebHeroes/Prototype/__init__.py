from LuaBridge import PrototypeDefinition

from Prototype.ResourceType import ResourceType
from Prototype.FieldType import FieldType
from Prototype.SettlementType import SettlementType
from Prototype.PlayerColorType import PlayerColorType

prototype_definitions: list[PrototypeDefinition] = [
    PrototypeDefinition(ResourceType, "resource"),
    PrototypeDefinition(FieldType, "field"),
    PrototypeDefinition(SettlementType, "settlement"),
    PrototypeDefinition(PlayerColorType, "player-color"),
]

__all__ = [
    "prototype_definitions",
    "ResourceType",
    "FieldType",
    "SettlementType",
]
