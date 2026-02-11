from LuaBridge import PrototypeDefinition

from Prototype.Resource import Resource

prototype_definitions: list[PrototypeDefinition] = [
    PrototypeDefinition(Resource, "resource"),
]

__all__ = [
    "prototype_definitions",
    "Resource",
]
