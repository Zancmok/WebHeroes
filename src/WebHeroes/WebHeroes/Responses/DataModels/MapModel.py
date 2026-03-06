from WebHeroes.Responses import BaseDataModel
from dataclasses import field, dataclass
from WebHeroes.Responses.DataModels.FieldModel import FieldModel


@dataclass
class MapModel(BaseDataModel):
    object_type: str = field(default="map-model", kw_only=True)

    fields: dict[str, FieldModel]
