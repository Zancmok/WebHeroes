from LuaBridge import BasePrototype
from .SettlementType import SettlementType
from .Ingredient import Ingredient


class Recipe(BasePrototype):
    def __init__(self, name: str, display_name: str, result: SettlementType, ingredients: list[Ingredient]) -> None:
        super().__init__(name, display_name)

        self.result: SettlementType = result
        self.ingredients: list[Ingredient] = ingredients
