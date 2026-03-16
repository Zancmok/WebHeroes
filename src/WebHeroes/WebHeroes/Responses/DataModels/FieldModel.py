from typing import Optional
from Prototype import FieldPrototype
from WebHeroes.Responses.BaseDataModel import BaseDataModel
from dataclasses import field, dataclass


@dataclass
class FieldModel(BaseDataModel):
    object_type: str = field(default="field-model", kw_only=True)

    field_type: FieldPrototype
    assigned_number: Optional[int]
