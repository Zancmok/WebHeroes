from LuaBridge import PrototypeDefinition

from Prototype.ResourceType import ResourceType
from Prototype.FieldType import FieldType

prototype_definitions: list[PrototypeDefinition] = [
    PrototypeDefinition(ResourceType, "resource"),
    PrototypeDefinition(FieldType, "field"),
]

__all__ = [
    "prototype_definitions",
    "ResourceType",
    "FieldType",
]
