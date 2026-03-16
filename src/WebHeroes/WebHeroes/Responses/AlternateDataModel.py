from typing import Any


class AlternateDataModel:
    def __init__(self) -> None:
        self.object_type: str = "alternate-data-model"

    def to_dictify(self) -> dict[str, Any]:
        return {
            "object_type": self.object_type
        }
