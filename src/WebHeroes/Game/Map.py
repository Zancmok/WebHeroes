import random

from Prototype import FieldType, SettingsType
from .Field import Field
from .Intersection import Intersection


class Map:
    def __init__(self, field_types: list[FieldType], settings_type: SettingsType) -> None:
        self.initial_field: Field

        tile_amount: int = settings_type.map_size + 2 * sum(range(3, settings_type.map_size))

        fields: list[FieldType] = []
        field_ranges: dict[range, FieldType] = {}

        total_weight: int = 0
        for field_type in field_types:
            for i in range(field_type.minimum_amount):
                fields.append(field_type)

            field_ranges[range(total_weight, total_weight + field_type.weight)] = field_type
            total_weight += field_type.weight

        for _ in range(len(fields), tile_amount):
            random_num: int = random.randint(0, total_weight - 1)

            for v in field_ranges:
                if random_num in v:
                    fields.append(field_ranges[v])
                    break

        random.shuffle(fields)

        self.initial_field = Field(fields[0])
