from .Field import Field


class Intersection:
    def __init__(self, fields: list[Field]) -> None:
        self.fields: list[Field] = fields
