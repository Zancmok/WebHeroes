from typing import override, Any
from .AbstractBasePrototype import AbstractBasePrototype
from .AbstractBuildingPrototype import AbstractBuildingPrototype
from .Ingredient import Ingredient


class Recipe(AbstractBasePrototype):
    def __init__(self, name: str, display_name: str, result: AbstractBuildingPrototype, ingredients: list[Ingredient]) -> None:
        super().__init__(name, display_name)
        self.object_type = "recipe-s_prototype"

        self.result: AbstractBuildingPrototype = result
        self.ingredients: list[Ingredient] = ingredients

    @override
    def to_dictify(self) -> dict[str, Any]:
        return {
            **super().to_dictify(),
            "result": self.result.to_dictify(),
            "ingredients": [
                ingredient.to_dictify()
                for ingredient in self.ingredients
            ]
        }
