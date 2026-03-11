from typing import Optional
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from WebHeroes.Responses.DataModels.FieldTypeModel import FieldTypeModel
from dataclasses import field, dataclass


@dataclass
class FieldModel(BaseDataModel):
    object_type: str = field(default="field-model", kw_only=True)

    field_type: FieldTypeModel
    q: int
    r: int
    assigned_number: Optional[int]
