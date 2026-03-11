from typing import Optional
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class ResourceTypeModel(BaseDataModel):
    object_type: str = field(default="resource-type-model", kw_only=True)

    name: str
    display_name: str
