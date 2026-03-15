from LuaBridge import BasePrototype
from .Ingredient import Ingredient


class Recipe(BasePrototype):
    def __init__(self, name: str, display_name: str, result: str, ingredients: list[Ingredient]) -> None:
        super().__init__(name, display_name)

        self.result: str = result
        self.ingredients: list[Ingredient] = ingredients
