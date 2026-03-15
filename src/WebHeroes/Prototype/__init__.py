from LuaBridge import PrototypeDefinition
from .SettingsPrototype import SettingsPrototype
from .Ingredient import Ingredient
from .Recipe import Recipe
from .PlayerColor import PlayerColor
from .FieldPrototype import FieldPrototype
from .ResourcePrototype import ResourcePrototype
from .SettlementPrototype import SettlementPrototype
from .RoadPrototype import RoadPrototype

prototype_definitions: list[PrototypeDefinition] = [
    PrototypeDefinition(SettingsPrototype, "settings"),
    PrototypeDefinition(Ingredient, "ingredient"),
    PrototypeDefinition(Recipe, "recipe"),
    PrototypeDefinition(PlayerColor, "player-color"),
    PrototypeDefinition(FieldPrototype, "field"),
    PrototypeDefinition(ResourcePrototype, "resource"),
    PrototypeDefinition(SettlementPrototype, "settlement"),
    PrototypeDefinition(RoadPrototype, "road")
]

__all__ = [
    "prototype_definitions",
    "SettingsPrototype",
    "Ingredient",
    "Recipe",
    "PlayerColor",
    "FieldPrototype",
    "ResourcePrototype",
    "SettlementPrototype",
    "RoadPrototype"
]
