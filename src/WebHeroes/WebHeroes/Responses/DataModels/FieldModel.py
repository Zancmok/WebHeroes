from typing import Optional
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class FieldModel(BaseDataModel):
    object_type: str = field(default="field-model", kw_only=True)

    field_type: str
    sprite: str
    resource: Optional[str]
    assigned_number: Optional[int]
