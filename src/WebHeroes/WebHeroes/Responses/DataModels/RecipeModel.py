from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class RecipeModel(BaseDataModel):
    object_type: str = field(default="recipe-model", kw_only=True)


