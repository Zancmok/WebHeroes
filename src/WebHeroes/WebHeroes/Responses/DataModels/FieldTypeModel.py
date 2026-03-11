from typing import Optional
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass
from WebHeroes.Responses.DataModels.ResourceTypeModel import ResourceTypeModel


@dataclass
class FieldTypeModel(BaseDataModel):
    object_type: str = field(default="field-type-model", kw_only=True)

    name: str
    display_name: str
    sprite: str
    weight: int
    minimum_amount: int
    resource: Optional[ResourceTypeModel]
