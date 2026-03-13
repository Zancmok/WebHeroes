from LuaBridge import PrototypeDefinition

from Prototype.ResourceType import ResourceType
from Prototype.FieldType import FieldType
from Prototype.SettlementType import SettlementType
from Prototype.PlayerColorType import PlayerColorType
from Prototype.SettingsType import SettingsType
from Prototype.Ingredient import Ingredient
from Prototype.Recipe import Recipe

prototype_definitions: list[PrototypeDefinition] = [
    PrototypeDefinition(ResourceType, "resource"),
    PrototypeDefinition(FieldType, "field"),
    PrototypeDefinition(SettlementType, "settlement"),
    PrototypeDefinition(PlayerColorType, "player-color"),
    PrototypeDefinition(SettingsType, "settings-type"),
    PrototypeDefinition(Ingredient, "ingredient"),
    PrototypeDefinition(Recipe, "recipe")
]

__all__ = [
    "prototype_definitions",
    "ResourceType",
    "FieldType",
    "SettlementType",
    "PlayerColorType",
    "SettingsType",
    "Ingredient",
    "Recipe"
]
